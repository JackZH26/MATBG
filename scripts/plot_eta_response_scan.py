#!/usr/bin/env python3
"""Plot eta-response scan diagnostics."""

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
        default=ROOT / "data" / "processed" / "eta_response_scan_nk7_nkeep6.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "figures" / "eta_response_scan_nk7_nkeep6.png",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=ROOT / "data" / "processed" / "eta_response_scan_nk7_nkeep6_summary.csv",
    )
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def group_by_normalization(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row["normalization"], []).append(row)
    for norm_rows in grouped.values():
        norm_rows.sort(key=lambda row: float(row["eta"]))
    return grouped


def float_column(rows: list[dict[str, str]], name: str) -> list[float]:
    return [float(row[name]) for row in rows]


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


def write_summary(path: Path, grouped: dict[str, list[dict[str, str]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "normalization",
        "eta_min",
        "eta_max",
        "W_pair_min",
        "W_pair_max",
        "D_iso_min",
        "D_iso_max",
        "D_iso_relative_change",
        "anisotropy_ratio_min",
        "anisotropy_ratio_max",
        "geom_fraction_min",
        "geom_fraction_max",
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for normalization, rows in grouped.items():
            d_values = [d_iso(row) for row in rows]
            geom_values = [geom_fraction(row) for row in rows]
            writer.writerow(
                {
                    "normalization": normalization,
                    "eta_min": min(float_column(rows, "eta")),
                    "eta_max": max(float_column(rows, "eta")),
                    "W_pair_min": min(float_column(rows, "interband_pairing_weight_mean")),
                    "W_pair_max": max(float_column(rows, "interband_pairing_weight_mean")),
                    "D_iso_min": min(d_values),
                    "D_iso_max": max(d_values),
                    "D_iso_relative_change": (d_values[-1] - d_values[0])
                    / d_values[0],
                    "anisotropy_ratio_min": min(float_column(rows, "anisotropy_ratio")),
                    "anisotropy_ratio_max": max(float_column(rows, "anisotropy_ratio")),
                    "geom_fraction_min": min(geom_values),
                    "geom_fraction_max": max(geom_values),
                }
            )


def main() -> int:
    args = parse_args()
    grouped = group_by_normalization(load_rows(args.input))
    write_summary(args.summary, grouped)

    labels = {
        "fixed_frobenius_norm": "fixed Frobenius norm",
        "fixed_delta0": "fixed Delta0",
    }
    colors = {
        "fixed_frobenius_norm": "#1f77b4",
        "fixed_delta0": "#d62728",
    }

    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.8), constrained_layout=True)
    ax_w, ax_d, ax_g, ax_a = axes.ravel()
    for normalization, rows in grouped.items():
        eta = float_column(rows, "eta")
        w_pair = float_column(rows, "interband_pairing_weight_mean")
        d_values = [d_iso(row) for row in rows]
        d_norm = [value / d_values[0] for value in d_values]
        geom_values = [geom_fraction(row) for row in rows]
        anisotropy = float_column(rows, "anisotropy_ratio")
        label = labels.get(normalization, normalization)
        color = colors.get(normalization)

        ax_w.plot(eta, w_pair, marker="o", label=label, color=color)
        ax_d.plot(eta, d_norm, marker="o", label=label, color=color)
        ax_g.plot(eta, geom_values, marker="o", label=label, color=color)
        ax_a.plot(eta, anisotropy, marker="o", label=label, color=color)

    ax_w.set_title("Projected interband pairing")
    ax_w.set_xlabel("eta")
    ax_w.set_ylabel("W_inter")
    ax_w.legend(frameon=False)

    ax_d.set_title("Isotropic total response")
    ax_d.set_xlabel("eta")
    ax_d.set_ylabel("D_iso / D_iso(0)")

    ax_g.set_title("Geometric fraction")
    ax_g.set_xlabel("eta")
    ax_g.set_ylabel("(Dxx_geom + Dyy_geom) / (Dxx + Dyy)")

    ax_a.set_title("Anisotropy")
    ax_a.set_xlabel("eta")
    ax_a.set_ylabel("Dxx / Dyy")
    ax_a.axhline(1.0, color="0.7", linewidth=1)

    for axis in axes.ravel():
        axis.grid(True, alpha=0.25)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180)
    pdf_output = args.output.with_suffix(".pdf")
    fig.savefig(pdf_output)
    print(f"Wrote {args.output}")
    print(f"Wrote {pdf_output}")
    print(f"Wrote {args.summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
