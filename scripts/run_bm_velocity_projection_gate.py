#!/usr/bin/env python3
"""Validate normal-state velocity projection and intra/inter splitting."""

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

from matbg.band_basis import (  # noqa: E402
    decomposition_error,
    hermitian_projection_error,
    offdiag_weight,
    split_intra_inter,
)
from matbg.bm_model import BMModel, BMParameters  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nk", type=int, default=3)
    parser.add_argument("--n-shell", type=int, default=3)
    parser.add_argument("--n-keep-values", type=int, nargs="+", default=[2, 4, 6])
    parser.add_argument("--dk", type=float, default=1.0e-6)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "bm_velocity_projection_gate.csv",
    )
    return parser.parse_args()


def summarize(values: list[float]) -> tuple[float, float, float, float]:
    array = np.asarray(values, dtype=float)
    return (
        float(np.mean(array)),
        float(np.std(array)),
        float(np.min(array)),
        float(np.max(array)),
    )


def main() -> int:
    args = parse_args()
    model = BMModel(BMParameters(n_shell=args.n_shell))
    mesh = model.centered_mesh(args.nk)

    rows: list[dict[str, object]] = []
    for n_keep in args.n_keep_values:
        for direction in ("x", "y"):
            herm_errors: list[float] = []
            split_errors: list[float] = []
            offdiag_weights: list[float] = []
            intra_norms: list[float] = []
            inter_norms: list[float] = []
            total_norms: list[float] = []

            for k_vec in mesh:
                _, vectors = model.selected_bands(k_vec, n_keep=n_keep)
                v_band = model.selected_velocity(
                    k_vec,
                    vectors,
                    direction=direction,
                    dk=args.dk,
                )
                intra, inter = split_intra_inter(v_band)
                herm_errors.append(hermitian_projection_error(v_band))
                split_errors.append(decomposition_error(v_band))
                offdiag_weights.append(offdiag_weight(v_band))
                intra_norms.append(float(np.linalg.norm(intra)))
                inter_norms.append(float(np.linalg.norm(inter)))
                total_norms.append(float(np.linalg.norm(v_band)))

            herm_mean, _, _, herm_max = summarize(herm_errors)
            split_mean, _, _, split_max = summarize(split_errors)
            weight_mean, weight_std, weight_min, weight_max = summarize(
                offdiag_weights
            )
            intra_mean, _, _, _ = summarize(intra_norms)
            inter_mean, _, _, _ = summarize(inter_norms)
            total_mean, _, _, _ = summarize(total_norms)
            rows.append(
                {
                    "nk": args.nk,
                    "n_shell": args.n_shell,
                    "n_keep": n_keep,
                    "direction": direction,
                    "dimension": model.dimension,
                    "dk_Ainv": args.dk,
                    "velocity_hermiticity_error_mean": herm_mean,
                    "velocity_hermiticity_error_max": herm_max,
                    "decomposition_error_mean": split_mean,
                    "decomposition_error_max": split_max,
                    "offdiag_velocity_weight_mean": weight_mean,
                    "offdiag_velocity_weight_std": weight_std,
                    "offdiag_velocity_weight_min": weight_min,
                    "offdiag_velocity_weight_max": weight_max,
                    "intra_velocity_norm_mean": intra_mean,
                    "inter_velocity_norm_mean": inter_mean,
                    "total_velocity_norm_mean": total_mean,
                }
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"BM dimension: {model.dimension}")
    print(f"Wrote {args.output}")
    print("n_keep dir offdiag_w herm_max split_max intra_norm inter_norm total_norm")
    for row in rows:
        print(
            f"{int(row['n_keep']):6d} "
            f"{str(row['direction']):>3s} "
            f"{float(row['offdiag_velocity_weight_mean']):9.6f} "
            f"{float(row['velocity_hermiticity_error_max']):8.1e} "
            f"{float(row['decomposition_error_max']):8.1e} "
            f"{float(row['intra_velocity_norm_mean']):10.3f} "
            f"{float(row['inter_velocity_norm_mean']):10.3f} "
            f"{float(row['total_velocity_norm_mean']):10.3f}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
