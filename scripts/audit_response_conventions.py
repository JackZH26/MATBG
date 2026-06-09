#!/usr/bin/env python3
"""Audit response sensitivity to Nambu-current conventions."""

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


MODES = [
    "intra_tauz_inter_tau0",
    "all_tauz",
    "all_tau0",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nk", type=int, default=14)
    parser.add_argument("--n-shell", type=int, default=3)
    parser.add_argument("--n-keep-values", type=int, nargs="+", default=[2, 6])
    parser.add_argument("--delta0", type=float, default=1.0)
    parser.add_argument("--mu", type=float, default=0.0)
    parser.add_argument("--dk", type=float, default=1.0e-6)
    parser.add_argument(
        "--benchmark",
        type=Path,
        default=ROOT / "data" / "processed" / "baseline_benchmarks.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "response_convention_audit_nk14.csv",
    )
    return parser.parse_args()


def nambu_block(particle: np.ndarray, hole_sign: float) -> np.ndarray:
    particle = np.asarray(particle, dtype=complex)
    zero = np.zeros_like(particle)
    hole = hole_sign * particle.T
    return np.block([[particle, zero], [zero, hole]]).reshape(
        2 * particle.shape[0],
        2 * particle.shape[0],
    )


def currents(velocity: np.ndarray, mode: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    intra, inter = split_intra_inter(velocity)
    if mode == "intra_tauz_inter_tau0":
        j_intra = nambu_block(intra, hole_sign=-1.0)
        j_inter = nambu_block(inter, hole_sign=1.0)
    elif mode == "all_tauz":
        j_intra = nambu_block(intra, hole_sign=-1.0)
        j_inter = nambu_block(inter, hole_sign=-1.0)
    elif mode == "all_tau0":
        j_intra = nambu_block(intra, hole_sign=1.0)
        j_inter = nambu_block(inter, hole_sign=1.0)
    else:
        raise ValueError(f"Unsupported mode: {mode}")
    return j_intra + j_inter, j_intra, j_inter


def average(values: list[float]) -> float:
    return float(np.mean(np.asarray(values, dtype=float)))


def load_benchmarks(path: Path) -> dict[int, float]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    benchmarks = {}
    for row in rows:
        if row["pairing"] != "uniform_s":
            continue
        if float(row["mu_meV"]) != 0.0 or float(row["delta0_meV"]) != 1.0:
            continue
        benchmarks[int(float(row["n_keep"]))] = float(row["D_total_eV_A2"])
    return benchmarks


def evaluate_mode(
    cache,
    n_keep: int,
    delta0: float,
    mu: float,
    mode: str,
) -> dict[str, float]:
    delta_band = delta0 * np.eye(n_keep, dtype=complex)
    values: dict[str, list[float]] = {
        "Dxx_total": [],
        "Dxx_conv": [],
        "Dxx_geom": [],
        "Dxx_cross": [],
        "Dyy_total": [],
        "Dyy_conv": [],
        "Dyy_geom": [],
        "Dyy_cross": [],
    }
    for item in cache:
        h_bdg = bdg_hamiltonian(item.eps, item.eps, delta_band, mu=mu)
        for prefix, velocity in (("Dxx", item.velocity_x), ("Dyy", item.velocity_y)):
            j_total, j_intra, j_inter = currents(velocity, mode)
            total = kubo_response(h_bdg, j_total)
            conv = kubo_response(h_bdg, j_intra)
            geom = kubo_response(h_bdg, j_inter)
            cross = total - conv - geom
            values[f"{prefix}_total"].append(total)
            values[f"{prefix}_conv"].append(conv)
            values[f"{prefix}_geom"].append(geom)
            values[f"{prefix}_cross"].append(cross)

    dxx_total = average(values["Dxx_total"])
    dyy_total = average(values["Dyy_total"])
    dxx_conv = average(values["Dxx_conv"])
    dyy_conv = average(values["Dyy_conv"])
    dxx_geom = average(values["Dxx_geom"])
    dyy_geom = average(values["Dyy_geom"])
    dxx_cross = average(values["Dxx_cross"])
    dyy_cross = average(values["Dyy_cross"])
    return {
        "D_iso_raw": 0.5 * (dxx_total + dyy_total),
        "Dconv_iso_raw": 0.5 * (dxx_conv + dyy_conv),
        "Dgeom_iso_raw": 0.5 * (dxx_geom + dyy_geom),
        "Dcross_iso_raw": 0.5 * (dxx_cross + dyy_cross),
        "anisotropy_ratio": dxx_total / dyy_total if dyy_total != 0 else np.nan,
    }


def main() -> int:
    args = parse_args()
    benchmarks = load_benchmarks(args.benchmark)
    model = BMModel(BMParameters(n_shell=args.n_shell))
    rows: list[dict[str, object]] = []
    for n_keep in args.n_keep_values:
        cache = build_response_cache(
            model=model,
            nk=args.nk,
            n_keep=n_keep,
            dk=args.dk,
        )
        for mode in MODES:
            result = evaluate_mode(
                cache=cache,
                n_keep=n_keep,
                delta0=args.delta0,
                mu=args.mu,
                mode=mode,
            )
            d_iso = raw_mev_a2_to_ev_a2(result["D_iso_raw"])
            dconv = raw_mev_a2_to_ev_a2(result["Dconv_iso_raw"])
            dgeom = raw_mev_a2_to_ev_a2(result["Dgeom_iso_raw"])
            dcross = raw_mev_a2_to_ev_a2(result["Dcross_iso_raw"])
            benchmark = benchmarks.get(n_keep, np.nan)
            rows.append(
                {
                    "mode": mode,
                    "nk": args.nk,
                    "n_keep": n_keep,
                    "D_iso_eV_A2": d_iso,
                    "Dconv_iso_eV_A2": dconv,
                    "Dgeom_iso_eV_A2": dgeom,
                    "Dcross_iso_eV_A2": dcross,
                    "geom_fraction": dgeom / d_iso if d_iso != 0 else np.nan,
                    "anisotropy_ratio": result["anisotropy_ratio"],
                    "benchmark_D_total_eV_A2": benchmark,
                    "relative_delta_to_benchmark": d_iso / benchmark - 1.0
                    if benchmark == benchmark
                    else np.nan,
                }
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {args.output}")
    for row in rows:
        print(
            f"n_keep={row['n_keep']} {row['mode']} "
            f"D_iso={float(row['D_iso_eV_A2']):.2f} "
            f"delta={100.0 * float(row['relative_delta_to_benchmark']):+.2f}%"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
