#!/usr/bin/env python3
"""Plot dense mu-eta response maps."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "data" / "processed" / "mu_eta_response_scan_nk7_nkeep6.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "figures" / "mu_eta_response_heatmap_nk7_nkeep6.png",
    )
    parser.add_argument("--normalization", default="fixed_frobenius_norm")
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def value(row: dict[str, str], key: str) -> float:
    return float(row[key])


def pivot(
    rows: list[dict[str, str]],
    key: str,
    normalizer: dict[float, float] | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mus = sorted({value(row, "mu_meV") for row in rows})
    etas = sorted({value(row, "eta") for row in rows})
    grid = np.full((len(etas), len(mus)), np.nan)
    for row in rows:
        eta = value(row, "eta")
        mu = value(row, "mu_meV")
        raw = value(row, key)
        if normalizer is not None:
            raw = raw / normalizer[mu] - 1.0
        grid[etas.index(eta), mus.index(mu)] = raw
    return np.asarray(mus), np.asarray(etas), grid


def main() -> int:
    args = parse_args()
    all_rows = load_rows(args.input)
    rows = [row for row in all_rows if row["normalization"] == args.normalization]
    if not rows:
        raise SystemExit(f"No rows for normalization {args.normalization}")

    baseline = {
        value(row, "mu_meV"): value(row, "D_iso_raw")
        for row in rows
        if abs(value(row, "eta")) < 1.0e-12
    }
    mus, etas, rel_d = pivot(rows, "D_iso_raw", normalizer=baseline)
    _, _, geom = pivot(rows, "geom_fraction_total")
    _, _, anis = pivot(rows, "anisotropy_ratio")

    fig, axes = plt.subplots(1, 3, figsize=(13.0, 3.8), constrained_layout=True)
    panels = [
        (rel_d, "D_iso / D_iso(eta=0) - 1", "RdBu_r"),
        (geom, "geometric fraction", "viridis"),
        (anis, "Dxx / Dyy", "coolwarm"),
    ]
    extent = [mus.min(), mus.max(), etas.min(), etas.max()]
    for axis, (grid, title, cmap) in zip(axes, panels):
        image = axis.imshow(
            grid,
            origin="lower",
            aspect="auto",
            extent=extent,
            cmap=cmap,
        )
        axis.set_title(title)
        axis.set_xlabel("mu (meV)")
        axis.set_ylabel("eta")
        fig.colorbar(image, ax=axis)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180)
    pdf_output = args.output.with_suffix(".pdf")
    fig.savefig(pdf_output)
    print(f"Wrote {args.output}")
    print(f"Wrote {pdf_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
