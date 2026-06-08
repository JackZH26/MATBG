#!/usr/bin/env python3
"""Diagnose how raw valley-minus eigenvectors overlap the TR-sewn target."""

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
from matbg.sewing import identity_time_reversal_target, procrustes_sew_subspace  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nk", type=int, default=3)
    parser.add_argument("--n-shell", type=int, default=3)
    parser.add_argument("--n-keep-values", type=int, nargs="+", default=[2, 4, 6])
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "valley_sewing_diagnostic.csv",
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
    plus = BMModel(BMParameters(n_shell=args.n_shell, valley=1))
    minus = BMModel(BMParameters(n_shell=args.n_shell, valley=-1))
    mesh = plus.centered_mesh(args.nk)

    rows: list[dict[str, object]] = []
    for n_keep in args.n_keep_values:
        errors: list[float] = []
        min_svs: list[float] = []
        mean_svs: list[float] = []
        for k_vec in mesh:
            _, u_plus = plus.selected_bands(k_vec, n_keep=n_keep)
            _, u_minus_raw = minus.selected_bands(-k_vec, n_keep=n_keep)
            sewing = procrustes_sew_subspace(
                u_minus_raw,
                identity_time_reversal_target(u_plus),
            )
            errors.append(sewing.alignment_error)
            min_svs.append(sewing.min_singular_value)
            mean_svs.append(sewing.mean_singular_value)

        err_mean, err_std, err_min, err_max = summarize(errors)
        min_sv_mean, min_sv_std, min_sv_min, min_sv_max = summarize(min_svs)
        mean_sv_mean, mean_sv_std, mean_sv_min, mean_sv_max = summarize(mean_svs)
        rows.append(
            {
                "nk": args.nk,
                "n_shell": args.n_shell,
                "n_keep": n_keep,
                "dimension": plus.dimension,
                "alignment_error_mean": err_mean,
                "alignment_error_std": err_std,
                "alignment_error_min": err_min,
                "alignment_error_max": err_max,
                "min_singular_mean": min_sv_mean,
                "min_singular_std": min_sv_std,
                "min_singular_min": min_sv_min,
                "min_singular_max": min_sv_max,
                "mean_singular_mean": mean_sv_mean,
                "mean_singular_std": mean_sv_std,
                "mean_singular_min": mean_sv_min,
                "mean_singular_max": mean_sv_max,
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"BM dimension: {plus.dimension}")
    print(f"Wrote {args.output}")
    print("n_keep err_mean err_max min_sv_mean min_sv_min mean_sv_mean")
    for row in rows:
        print(
            f"{int(row['n_keep']):6d} "
            f"{float(row['alignment_error_mean']):8.4f} "
            f"{float(row['alignment_error_max']):8.4f} "
            f"{float(row['min_singular_mean']):11.4f} "
            f"{float(row['min_singular_min']):10.4f} "
            f"{float(row['mean_singular_mean']):12.4f}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
