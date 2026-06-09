#!/usr/bin/env python3
"""Reconstruct PRB-style uniform-s benchmark tables from explicit candidates."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from matbg.band_basis import split_intra_inter  # noqa: E402
from matbg.bm_model import BMModel, BMParameters  # noqa: E402
from matbg.pairing import bdg_hamiltonian  # noqa: E402
from matbg.response_scan import build_response_cache  # noqa: E402
from matbg.stiffness import kubo_response  # noqa: E402
from matbg.units import raw_mev_a2_to_ev_a2  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nk", type=int, default=14)
    parser.add_argument("--n-shell", type=int, default=3)
    parser.add_argument("--n-keep-values", type=int, nargs="+", default=[2, 4, 6])
    parser.add_argument("--theta-deg", type=float, default=1.05)
    parser.add_argument("--vF-eV-A", type=float, default=2.135)
    parser.add_argument("--w0-meV", type=float, default=87.2)
    parser.add_argument("--w1-meV", type=float, default=109.0)
    parser.add_argument("--delta0", type=float, default=1.0)
    parser.add_argument("--mu", type=float, default=0.0)
    parser.add_argument("--velocity-dk", type=float, default=1.0e-6)
    parser.add_argument("--curvature-dk", type=float, default=1.0e-4)
    parser.add_argument(
        "--targets",
        type=Path,
        default=ROOT / "data" / "processed" / "prb_manuscript_targets.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "prb_table_reconstruction_nk14.csv",
    )
    return parser.parse_args()


def optional_float(value: str) -> float | None:
    if value == "":
        return None
    return float(value)


def load_targets(path: Path) -> dict[int, dict[str, float | None]]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    targets: dict[int, dict[str, float | None]] = {}
    for row in rows:
        if row["pairing"] != "uniform_s":
            continue
        if optional_float(row["mu_meV"]) != 0.0:
            continue
        if optional_float(row["delta0_meV"]) != 1.0:
            continue
        targets[int(float(row["n_keep"]))] = {
            "D_total_eV_A2": optional_float(row["D_total_eV_A2"]),
            "D_conv_eV_A2": optional_float(row["D_conv_eV_A2"]),
            "D_geom_eV_A2": optional_float(row["D_geom_eV_A2"]),
            "geom_fraction": optional_float(row["geom_fraction"]),
        }
    return targets


def average(values: list[float]) -> float:
    return float(np.mean(np.asarray(values, dtype=float)))


def nambu_block(particle: np.ndarray, hole_sign: float) -> np.ndarray:
    particle = np.asarray(particle, dtype=complex)
    zero = np.zeros_like(particle)
    hole = hole_sign * particle.T
    return np.block([[particle, zero], [zero, hole]]).reshape(
        2 * particle.shape[0],
        2 * particle.shape[0],
    )


def curvature_for_direction(
    model: BMModel,
    k_vec: np.ndarray,
    eps: np.ndarray,
    n_keep: int,
    direction: np.ndarray,
) -> np.ndarray:
    eps_plus, _ = model.selected_bands(k_vec + direction, n_keep=n_keep)
    eps_minus, _ = model.selected_bands(k_vec - direction, n_keep=n_keep)
    step = float(np.linalg.norm(direction))
    return (eps_plus - 2.0 * eps + eps_minus) / (step * step)


def component_baselines(
    model: BMModel,
    nk: int,
    n_keep: int,
    delta0: float,
    mu: float,
    velocity_dk: float,
    curvature_dk: float,
) -> dict[str, float]:
    cache = build_response_cache(
        model=model,
        nk=nk,
        n_keep=n_keep,
        dk=velocity_dk,
    )
    delta_band = delta0 * np.eye(n_keep, dtype=complex)
    values: dict[str, list[float]] = {
        "conv_tauz_x": [],
        "conv_tauz_y": [],
        "geom_tau0_x": [],
        "geom_tau0_y": [],
        "geom_tauz_x": [],
        "geom_tauz_y": [],
        "curv_x": [],
        "curv_y": [],
    }

    for item in cache:
        h_bdg = bdg_hamiltonian(item.eps, item.eps, delta_band, mu=mu)
        xi = item.eps - mu
        energy = np.sqrt(xi * xi + delta0 * delta0)
        occupancy_weight = 1.0 - xi / energy

        for axis, velocity in (("x", item.velocity_x), ("y", item.velocity_y)):
            intra, inter = split_intra_inter(velocity)
            j_intra_tauz = nambu_block(intra, hole_sign=-1.0)
            j_inter_tau0 = nambu_block(inter, hole_sign=1.0)
            j_inter_tauz = nambu_block(inter, hole_sign=-1.0)
            values[f"conv_tauz_{axis}"].append(kubo_response(h_bdg, j_intra_tauz))
            values[f"geom_tau0_{axis}"].append(kubo_response(h_bdg, j_inter_tau0))
            values[f"geom_tauz_{axis}"].append(kubo_response(h_bdg, j_inter_tauz))

        kappa_x = curvature_for_direction(
            model=model,
            k_vec=item.k_vec,
            eps=item.eps,
            n_keep=n_keep,
            direction=np.array([curvature_dk, 0.0]),
        )
        kappa_y = curvature_for_direction(
            model=model,
            k_vec=item.k_vec,
            eps=item.eps,
            n_keep=n_keep,
            direction=np.array([0.0, curvature_dk]),
        )
        values["curv_x"].append(float(np.sum(kappa_x * occupancy_weight)))
        values["curv_y"].append(float(np.sum(kappa_y * occupancy_weight)))

    result = {}
    for key in ("conv_tauz", "geom_tau0", "geom_tauz", "curv"):
        result[key] = raw_mev_a2_to_ev_a2(
            0.5 * (average(values[f"{key}_x"]) + average(values[f"{key}_y"]))
        )
    return result


def candidate_rows(
    n_keep: int,
    components: dict[str, float],
    targets: dict[int, dict[str, float | None]],
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    conv = components["conv_tauz"]
    geom_tau0 = components["geom_tau0"]
    geom_tauz = components["geom_tauz"]
    curv = components["curv"]
    candidates = {
        "current_tauz_tau0": (conv, geom_tau0),
        "all_tauz": (conv, geom_tauz),
        "double_conv_all_tauz": (2.0 * conv, geom_tauz),
        "double_conv_half_curv_all_tauz": (2.0 * conv + 0.5 * curv, geom_tauz),
        "double_conv_full_curv_all_tauz": (2.0 * conv + curv, geom_tauz),
        "double_conv_tau0_geom": (2.0 * conv, geom_tau0),
    }

    target = targets.get(n_keep, {})
    rows = []
    for mode, (d_conv, d_geom) in candidates.items():
        d_total = d_conv + d_geom
        geom_fraction = d_geom / d_total if d_total != 0 else np.nan
        rows.append(
            {
                "mode": mode,
                "theta_deg": args.theta_deg,
                "nk": args.nk,
                "n_shell": args.n_shell,
                "n_keep": n_keep,
                "delta0_meV": args.delta0,
                "mu_meV": args.mu,
                "curvature_dk_Ainv": args.curvature_dk,
                "D_total_eV_A2": d_total,
                "D_conv_eV_A2": d_conv,
                "D_geom_eV_A2": d_geom,
                "geom_fraction": geom_fraction,
                "target_D_total_eV_A2": target.get("D_total_eV_A2"),
                "target_D_conv_eV_A2": target.get("D_conv_eV_A2"),
                "target_D_geom_eV_A2": target.get("D_geom_eV_A2"),
                "target_geom_fraction": target.get("geom_fraction"),
                "D_total_relative_delta": relative_delta(
                    d_total,
                    target.get("D_total_eV_A2"),
                ),
                "D_conv_relative_delta": relative_delta(
                    d_conv,
                    target.get("D_conv_eV_A2"),
                ),
                "D_geom_relative_delta": relative_delta(
                    d_geom,
                    target.get("D_geom_eV_A2"),
                ),
                "geom_fraction_delta": absolute_delta(
                    geom_fraction,
                    target.get("geom_fraction"),
                ),
            }
        )
    return rows


def relative_delta(value: float, target: float | None) -> float | str:
    if target is None:
        return ""
    return value / target - 1.0


def absolute_delta(value: float, target: float | None) -> float | str:
    if target is None:
        return ""
    return value - target


def sort_key(row: dict[str, object]) -> tuple[int, str]:
    return int(row["n_keep"]), str(row["mode"])


def main() -> int:
    args = parse_args()
    targets = load_targets(args.targets)
    model = BMModel(
        BMParameters(
            theta_deg=args.theta_deg,
            vF_eV_A=args.vF_eV_A,
            w0_meV=args.w0_meV,
            w1_meV=args.w1_meV,
            n_shell=args.n_shell,
        )
    )
    rows: list[dict[str, object]] = []
    for n_keep in args.n_keep_values:
        components = component_baselines(
            model=model,
            nk=args.nk,
            n_keep=n_keep,
            delta0=args.delta0,
            mu=args.mu,
            velocity_dk=args.velocity_dk,
            curvature_dk=args.curvature_dk,
        )
        rows.extend(candidate_rows(n_keep, components, targets, args))
    rows.sort(key=sort_key)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {args.output}")
    preferred = {"current_tauz_tau0", "all_tauz", "double_conv_all_tauz"}
    for row in rows:
        if row["mode"] not in preferred:
            continue
        total_delta = row["D_total_relative_delta"]
        conv_delta = row["D_conv_relative_delta"]
        print(
            f"n_keep={row['n_keep']} {row['mode']} "
            f"D={float(row['D_total_eV_A2']):.2f} "
            f"conv={float(row['D_conv_eV_A2']):.2f} "
            f"geom={float(row['D_geom_eV_A2']):.2f} "
            f"total_delta={total_delta if total_delta == '' else f'{100.0 * float(total_delta):+.2f}%'} "
            f"conv_delta={conv_delta if conv_delta == '' else f'{100.0 * float(conv_delta):+.2f}%'}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
