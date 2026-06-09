#!/usr/bin/env python3
"""Audit conventional-channel formula candidates against PRB benchmarks."""

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

from matbg.bm_model import BMModel, BMParameters  # noqa: E402
from matbg.response_scan import build_response_cache  # noqa: E402
from matbg.units import raw_mev_a2_to_ev_a2  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nk", type=int, default=14)
    parser.add_argument("--n-shell", type=int, default=3)
    parser.add_argument("--n-keep-values", type=int, nargs="+", default=[2, 6])
    parser.add_argument("--curvature-dk-values", type=float, nargs="+", default=[1.0e-4])
    parser.add_argument("--delta0", type=float, default=1.0)
    parser.add_argument("--mu", type=float, default=0.0)
    parser.add_argument("--velocity-dk", type=float, default=1.0e-6)
    parser.add_argument(
        "--benchmark",
        type=Path,
        default=ROOT / "data" / "processed" / "baseline_benchmarks.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "conventional_channel_audit_nk14.csv",
    )
    return parser.parse_args()


def average(values: list[float]) -> float:
    return float(np.mean(np.asarray(values, dtype=float)))


def load_uniform_conv_benchmarks(path: Path) -> dict[int, float]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    benchmarks = {}
    for row in rows:
        if row["pairing"] != "uniform_s":
            continue
        if float(row["mu_meV"]) != 0.0 or float(row["delta0_meV"]) != 1.0:
            continue
        benchmarks[int(float(row["n_keep"]))] = float(row["D_conv_eV_A2"])
    return benchmarks


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


def candidate_values(
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
    values: dict[str, list[float]] = {
        "para_x": [],
        "para_y": [],
        "curv_full_x": [],
        "curv_full_y": [],
    }
    for item in cache:
        xi = item.eps - mu
        energy = np.sqrt(xi * xi + delta0 * delta0)
        vx = np.real(np.diag(item.velocity_x))
        vy = np.real(np.diag(item.velocity_y))
        values["para_x"].append(float(np.sum(vx * vx * delta0 * delta0 / energy**3)))
        values["para_y"].append(float(np.sum(vy * vy * delta0 * delta0 / energy**3)))

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
        occupancy_weight = 1.0 - xi / energy
        values["curv_full_x"].append(float(np.sum(kappa_x * occupancy_weight)))
        values["curv_full_y"].append(float(np.sum(kappa_y * occupancy_weight)))

    para = raw_mev_a2_to_ev_a2(0.5 * (average(values["para_x"]) + average(values["para_y"])))
    curv_full = raw_mev_a2_to_ev_a2(
        0.5 * (average(values["curv_full_x"]) + average(values["curv_full_y"]))
    )
    curv_half = 0.5 * curv_full
    return {
        "paramagnetic_tauz": para,
        "two_paramagnetic_tauz": 2.0 * para,
        "curvature_full": curv_full,
        "curvature_half": curv_half,
        "paramagnetic_plus_curvature_full": para + curv_full,
        "paramagnetic_plus_curvature_half": para + curv_half,
        "two_paramagnetic_plus_curvature_half": 2.0 * para + curv_half,
        "two_paramagnetic_plus_curvature_full": 2.0 * para + curv_full,
    }


def main() -> int:
    args = parse_args()
    benchmarks = load_uniform_conv_benchmarks(args.benchmark)
    model = BMModel(BMParameters(n_shell=args.n_shell))
    rows: list[dict[str, object]] = []
    for n_keep in args.n_keep_values:
        benchmark = benchmarks.get(n_keep)
        if benchmark is None:
            continue
        for curvature_dk in args.curvature_dk_values:
            candidates = candidate_values(
                model=model,
                nk=args.nk,
                n_keep=n_keep,
                delta0=args.delta0,
                mu=args.mu,
                velocity_dk=args.velocity_dk,
                curvature_dk=curvature_dk,
            )
            for name, value in candidates.items():
                rows.append(
                    {
                        "candidate": name,
                        "nk": args.nk,
                        "n_keep": n_keep,
                        "curvature_dk_Ainv": curvature_dk,
                        "Dconv_candidate_eV_A2": value,
                        "Dconv_benchmark_eV_A2": benchmark,
                        "relative_delta_to_benchmark": value / benchmark - 1.0,
                    }
                )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {args.output}")
    for row in rows:
        if row["candidate"] in (
            "paramagnetic_tauz",
            "two_paramagnetic_tauz",
            "two_paramagnetic_plus_curvature_half",
            "two_paramagnetic_plus_curvature_full",
        ):
            print(
                f"n_keep={row['n_keep']} {row['candidate']} "
                f"Dconv={float(row['Dconv_candidate_eV_A2']):.2f} "
                f"delta={100.0 * float(row['relative_delta_to_benchmark']):+.2f}%"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
