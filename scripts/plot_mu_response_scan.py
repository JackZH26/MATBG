#!/usr/bin/env python3
"""Plot first mu-response scan diagnostics."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "data" / "processed" / "mu_response_scan_nk7_nkeep6.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "figures" / "mu_response_scan_nk7_nkeep6.png",
    )
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def d_iso(row: dict[str, str]) -> float:
    if "D_iso_raw" in row and row["D_iso_raw"]:
        return float(row["D_iso_raw"])
    return 0.5 * (float(row["Dxx_total_raw"]) + float(row["Dyy_total_raw"]))


def geom_fraction(row: dict[str, str]) -> float:
    if "geom_fraction_total" in row and row["geom_fraction_total"]:
        return float(row["geom_fraction_total"])
    geom = float(row["Dxx_geom_raw"]) + float(row["Dyy_geom_raw"])
    total = float(row["Dxx_total_raw"]) + float(row["Dyy_total_raw"])
    return geom / total if total else 0.0


def rows_for(
    rows: list[dict[str, str]],
    normalization: str,
    eta: float,
) -> list[dict[str, str]]:
    selected = [
        row
        for row in rows
        if row["normalization"] == normalization and abs(float(row["eta"]) - eta) < 1e-12
    ]
    selected.sort(key=lambda row: float(row["mu_meV"]))
    return selected


def main() -> int:
    args = parse_args()
    rows = load_rows(args.input)
    etas = sorted({float(row["eta"]) for row in rows})
    normalizations = ["fixed_frobenius_norm", "fixed_delta0"]
    titles = {
        "fixed_frobenius_norm": "fixed Frobenius norm",
        "fixed_delta0": "fixed Delta0",
    }
    colors = {0.0: "#333333", 0.5: "#1f77b4", 1.0: "#d62728"}

    fig, axes = plt.subplots(2, 2, figsize=(9.6, 7.0), constrained_layout=True)
    for col, normalization in enumerate(normalizations):
        ax_d = axes[0, col]
        ax_g = axes[1, col]
        for eta in etas:
            selected = rows_for(rows, normalization, eta)
            x_values = [
                float(row["nu_proxy"]) if "nu_proxy" in row and row["nu_proxy"] else float(row["mu_meV"])
                for row in selected
            ]
            d_values = [d_iso(row) for row in selected]
            geom_values = [geom_fraction(row) for row in selected]
            ax_d.plot(x_values, d_values, marker="o", label=f"eta={eta:g}", color=colors.get(eta))
            ax_g.plot(x_values, geom_values, marker="o", label=f"eta={eta:g}", color=colors.get(eta))

        ax_d.set_title(titles[normalization])
        ax_d.set_xlabel("nu proxy")
        ax_d.set_ylabel("D_iso raw")
        ax_d.grid(True, alpha=0.25)
        ax_d.legend(frameon=False)

        ax_g.set_xlabel("nu proxy")
        ax_g.set_ylabel("geometric fraction")
        ax_g.grid(True, alpha=0.25)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180)
    pdf_output = args.output.with_suffix(".pdf")
    fig.savefig(pdf_output)
    print(f"Wrote {args.output}")
    print(f"Wrote {pdf_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
