#!/usr/bin/env python3
"""Audit the unreconciled n_keep=2 PRB flat-band endpoint."""

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
from matbg.stiffness import kubo_response  # noqa: E402
from matbg.units import raw_mev_a2_to_ev_a2  # noqa: E402


TARGET_TOTAL = 67.5
TARGET_CONV = 53.0
TARGET_GEOM = 14.5
TARGET_GEOM_FRACTION = 0.215


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nk", type=int, default=14)
    parser.add_argument("--n-shell-values", type=int, nargs="+", default=[3])
    parser.add_argument("--theta-values", type=float, nargs="+", default=[1.05])
    parser.add_argument("--delta0", type=float, default=1.0)
    parser.add_argument("--mu", type=float, default=0.0)
    parser.add_argument("--velocity-dk", type=float, default=1.0e-6)
    parser.add_argument("--curvature-dk", type=float, default=1.0e-4)
    parser.add_argument(
        "--mesh-variants",
        nargs="+",
        default=["half_shift_centered", "gamma_centered", "positive_half_shift"],
    )
    parser.add_argument(
        "--band-selectors",
        nargs="+",
        default=["central_pair", "closest_abs", "valence_conduction"],
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "flatband_endpoint_audit_nk14.csv",
    )
    return parser.parse_args()


def average(values: list[float]) -> float:
    return float(np.mean(np.asarray(values, dtype=float)))


def fractional_values(nk: int, variant: str) -> np.ndarray:
    if variant == "half_shift_centered":
        return (np.arange(nk) - (nk - 1) / 2.0) / nk
    if variant == "gamma_centered":
        return (np.arange(nk) - nk // 2) / nk
    if variant == "positive_half_shift":
        return (np.arange(nk) + 0.5) / nk
    if variant == "positive_gamma":
        return np.arange(nk) / nk
    raise ValueError(f"Unsupported mesh variant: {variant}")


def mesh(model: BMModel, nk: int, variant: str) -> np.ndarray:
    values = fractional_values(nk, variant)
    return np.array(
        [model.fractional_k(x, y) for x in values for y in values],
        dtype=float,
    )


def selected_indices(energies: np.ndarray, selector: str) -> np.ndarray:
    n = energies.size
    center = n // 2
    if selector == "central_pair":
        return np.array([center - 1, center])
    if selector == "closest_abs":
        selected = np.argsort(np.abs(energies))[:2]
        return selected[np.argsort(energies[selected])]
    if selector == "valence_conduction":
        valence = np.where(energies <= 0.0)[0]
        conduction = np.where(energies > 0.0)[0]
        if valence.size == 0 or conduction.size == 0:
            return np.array([center - 1, center])
        return np.array([valence[-1], conduction[0]])
    raise ValueError(f"Unsupported band selector: {selector}")


def selected_bands(
    model: BMModel,
    k_vec: np.ndarray,
    selector: str,
) -> tuple[np.ndarray, np.ndarray]:
    energies, vectors = model.eigensystem(k_vec)
    selected = selected_indices(energies, selector)
    return energies[selected], vectors[:, selected]


def selected_velocity(
    model: BMModel,
    k_vec: np.ndarray,
    vectors: np.ndarray,
    direction: str,
    dk: float,
) -> np.ndarray:
    velocity = model.velocity_operator(k_vec, direction=direction, dk=dk)
    return vectors.conj().T @ velocity @ vectors


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
    selector: str,
    direction: np.ndarray,
) -> np.ndarray:
    eps_plus, _ = selected_bands(model, k_vec + direction, selector)
    eps_minus, _ = selected_bands(model, k_vec - direction, selector)
    step = float(np.linalg.norm(direction))
    return (eps_plus - 2.0 * eps + eps_minus) / (step * step)


def evaluate_case(
    model: BMModel,
    nk: int,
    mesh_variant: str,
    band_selector: str,
    delta0: float,
    mu: float,
    velocity_dk: float,
    curvature_dk: float,
) -> dict[str, float]:
    values: dict[str, list[float]] = {
        "conv_x": [],
        "conv_y": [],
        "geom_tauz_x": [],
        "geom_tauz_y": [],
        "geom_tau0_x": [],
        "geom_tau0_y": [],
        "curv_x": [],
        "curv_y": [],
    }
    bandwidth_values: list[float] = []
    delta_band = delta0 * np.eye(2, dtype=complex)
    for k_vec in mesh(model, nk, mesh_variant):
        eps, vectors = selected_bands(model, k_vec, band_selector)
        bandwidth_values.extend(eps.tolist())
        h_bdg = bdg_hamiltonian(eps, eps, delta_band, mu=mu)
        xi = eps - mu
        energy = np.sqrt(xi * xi + delta0 * delta0)
        occupancy_weight = 1.0 - xi / energy
        velocity_x = selected_velocity(model, k_vec, vectors, "x", velocity_dk)
        velocity_y = selected_velocity(model, k_vec, vectors, "y", velocity_dk)

        for axis, velocity in (("x", velocity_x), ("y", velocity_y)):
            intra, inter = split_intra_inter(velocity)
            j_intra = nambu_block(intra, hole_sign=-1.0)
            j_inter_tauz = nambu_block(inter, hole_sign=-1.0)
            j_inter_tau0 = nambu_block(inter, hole_sign=1.0)
            values[f"conv_{axis}"].append(kubo_response(h_bdg, j_intra))
            values[f"geom_tauz_{axis}"].append(kubo_response(h_bdg, j_inter_tauz))
            values[f"geom_tau0_{axis}"].append(kubo_response(h_bdg, j_inter_tau0))

        kappa_x = curvature_for_direction(
            model,
            k_vec,
            eps,
            band_selector,
            np.array([curvature_dk, 0.0]),
        )
        kappa_y = curvature_for_direction(
            model,
            k_vec,
            eps,
            band_selector,
            np.array([0.0, curvature_dk]),
        )
        values["curv_x"].append(float(np.sum(kappa_x * occupancy_weight)))
        values["curv_y"].append(float(np.sum(kappa_y * occupancy_weight)))

    conv = raw_mev_a2_to_ev_a2(0.5 * (average(values["conv_x"]) + average(values["conv_y"])))
    geom_tauz = raw_mev_a2_to_ev_a2(
        0.5 * (average(values["geom_tauz_x"]) + average(values["geom_tauz_y"]))
    )
    geom_tau0 = raw_mev_a2_to_ev_a2(
        0.5 * (average(values["geom_tau0_x"]) + average(values["geom_tau0_y"]))
    )
    curv = raw_mev_a2_to_ev_a2(0.5 * (average(values["curv_x"]) + average(values["curv_y"])))
    return {
        "bandwidth_meV": float(max(bandwidth_values) - min(bandwidth_values)),
        "conv_tauz": conv,
        "geom_tauz": geom_tauz,
        "geom_tau0": geom_tau0,
        "curvature": curv,
    }


def candidate_rows(base: dict[str, float]) -> list[tuple[str, float, float]]:
    conv = base["conv_tauz"]
    geom_tauz = base["geom_tauz"]
    geom_tau0 = base["geom_tau0"]
    curv = base["curvature"]
    return [
        ("current_tauz_tau0", conv, geom_tau0),
        ("all_tauz", conv, geom_tauz),
        ("double_conv_all_tauz", 2.0 * conv, geom_tauz),
        ("double_conv_half_curv_all_tauz", 2.0 * conv + 0.5 * curv, geom_tauz),
        ("double_conv_full_curv_all_tauz", 2.0 * conv + curv, geom_tauz),
    ]


def main() -> int:
    args = parse_args()
    rows: list[dict[str, object]] = []
    for n_shell in args.n_shell_values:
        for theta in args.theta_values:
            model = BMModel(BMParameters(theta_deg=theta, n_shell=n_shell))
            for mesh_variant in args.mesh_variants:
                for band_selector in args.band_selectors:
                    base = evaluate_case(
                        model=model,
                        nk=args.nk,
                        mesh_variant=mesh_variant,
                        band_selector=band_selector,
                        delta0=args.delta0,
                        mu=args.mu,
                        velocity_dk=args.velocity_dk,
                        curvature_dk=args.curvature_dk,
                    )
                    for candidate, d_conv, d_geom in candidate_rows(base):
                        d_total = d_conv + d_geom
                        geom_fraction = d_geom / d_total if d_total != 0 else np.nan
                        rows.append(
                            {
                                "candidate": candidate,
                                "theta_deg": theta,
                                "n_shell": n_shell,
                                "nk": args.nk,
                                "mesh_variant": mesh_variant,
                                "band_selector": band_selector,
                                "bandwidth_meV": base["bandwidth_meV"],
                                "D_total_eV_A2": d_total,
                                "D_conv_eV_A2": d_conv,
                                "D_geom_eV_A2": d_geom,
                                "geom_fraction": geom_fraction,
                                "target_D_total_eV_A2": TARGET_TOTAL,
                                "target_D_conv_eV_A2": TARGET_CONV,
                                "target_D_geom_eV_A2": TARGET_GEOM,
                                "target_geom_fraction": TARGET_GEOM_FRACTION,
                                "D_total_relative_delta": d_total / TARGET_TOTAL - 1.0,
                                "D_conv_relative_delta": d_conv / TARGET_CONV - 1.0,
                                "D_geom_relative_delta": d_geom / TARGET_GEOM - 1.0,
                                "geom_fraction_delta": geom_fraction - TARGET_GEOM_FRACTION,
                            }
                        )

    rows.sort(
        key=lambda row: (
            abs(float(row["D_total_relative_delta"]))
            + abs(float(row["D_conv_relative_delta"]))
            + abs(float(row["D_geom_relative_delta"])),
            str(row["candidate"]),
        )
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {args.output}")
    for row in rows[:10]:
        print(
            f"{row['candidate']} theta={float(row['theta_deg']):.3f} "
            f"mesh={row['mesh_variant']} selector={row['band_selector']} "
            f"W={float(row['bandwidth_meV']):.2f} "
            f"D={float(row['D_total_eV_A2']):.2f} "
            f"conv={float(row['D_conv_eV_A2']):.2f} "
            f"geom={float(row['D_geom_eV_A2']):.2f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
