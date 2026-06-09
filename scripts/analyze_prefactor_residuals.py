#!/usr/bin/env python3
"""Analyze whether simple prefactors can reconcile baseline responses."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ZERO_TOL = 1.0e-12


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audit",
        type=Path,
        default=ROOT / "data" / "processed" / "response_convention_audit_nk14.csv",
    )
    parser.add_argument(
        "--benchmark",
        type=Path,
        default=ROOT / "data" / "processed" / "baseline_benchmarks.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "prefactor_residual_audit_nk14.csv",
    )
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def uniform_benchmarks(path: Path) -> dict[int, dict[str, float]]:
    benchmarks = {}
    for row in load_rows(path):
        if row["pairing"] != "uniform_s":
            continue
        n_keep = int(float(row["n_keep"]))
        benchmarks[n_keep] = {
            "D_total": float(row["D_total_eV_A2"]),
            "D_conv": float(row["D_conv_eV_A2"]),
            "D_geom": float(row["D_geom_eV_A2"]),
        }
    return benchmarks


def fit_component_scales(rows: list[dict[str, str]], benchmarks: dict[int, dict[str, float]]) -> tuple[float, float]:
    matrix = []
    target = []
    for row in rows:
        n_keep = int(float(row["n_keep"]))
        if n_keep not in benchmarks:
            continue
        matrix.append(
            [
                float(row["Dconv_iso_eV_A2"]),
                float(row["Dgeom_iso_eV_A2"]),
            ]
        )
        target.append(benchmarks[n_keep]["D_total"])
    if not matrix:
        return float("nan"), float("nan")
    coeff, *_ = np.linalg.lstsq(np.asarray(matrix), np.asarray(target), rcond=None)
    return float(coeff[0]), float(coeff[1])


def main() -> int:
    args = parse_args()
    benchmarks = uniform_benchmarks(args.benchmark)
    audit_rows = load_rows(args.audit)
    modes = sorted({row["mode"] for row in audit_rows})
    fitted = {
        mode: fit_component_scales(
            [row for row in audit_rows if row["mode"] == mode],
            benchmarks,
        )
        for mode in modes
    }

    output_rows: list[dict[str, object]] = []
    for row in audit_rows:
        n_keep = int(float(row["n_keep"]))
        if n_keep not in benchmarks:
            continue
        bench = benchmarks[n_keep]
        total = float(row["D_iso_eV_A2"])
        conv = float(row["Dconv_iso_eV_A2"])
        geom = float(row["Dgeom_iso_eV_A2"])
        conv_fit, geom_fit = fitted[row["mode"]]
        fitted_total = conv_fit * conv + geom_fit * geom
        output_rows.append(
            {
                "mode": row["mode"],
                "n_keep": n_keep,
                "current_total_eV_A2": total,
                "benchmark_total_eV_A2": bench["D_total"],
                "total_scale_needed": bench["D_total"] / total,
                "current_conv_eV_A2": conv,
                "benchmark_conv_eV_A2": bench["D_conv"],
                "conv_scale_needed": bench["D_conv"] / conv
                if abs(conv) > ZERO_TOL
                else np.nan,
                "current_geom_eV_A2": geom,
                "benchmark_geom_eV_A2": bench["D_geom"],
                "geom_scale_needed": bench["D_geom"] / geom
                if abs(geom) > ZERO_TOL
                else np.nan,
                "least_squares_conv_scale_for_total": conv_fit,
                "least_squares_geom_scale_for_total": geom_fit,
                "least_squares_total_eV_A2": fitted_total,
                "least_squares_relative_error": fitted_total / bench["D_total"] - 1.0,
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0].keys()))
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Wrote {args.output}")
    for row in output_rows:
        print(
            f"{row['mode']} n_keep={row['n_keep']} "
            f"total_scale={float(row['total_scale_needed']):.3f} "
            f"conv_scale={float(row['conv_scale_needed']):.3f} "
            f"geom_scale={float(row['geom_scale_needed']):.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
