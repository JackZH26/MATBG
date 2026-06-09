#!/usr/bin/env python3
"""Plot selected-grid convergence of eta=1 response key points."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "figures" / "nk_convergence_keypoints_nkeep6.png",
    )
    return parser.parse_args()


def summary_path(nk: int) -> Path:
    return (
        ROOT
        / "data"
        / "processed"
        / f"mu_response_scan_nk{nk}_nkeep6_keypoints_summary.csv"
    )


def load_grid(nks: list[int]) -> dict[tuple[str, float], dict[int, float]]:
    data: dict[tuple[str, float], dict[int, float]] = {}
    for nk in nks:
        with summary_path(nk).open(newline="") as handle:
            for row in csv.DictReader(handle):
                key = (row["normalization"], float(row["mu_meV"]))
                data.setdefault(key, {})[nk] = (
                    100.0 * float(row["D_iso_rel_target_vs_baseline"])
                )
    return data


def main() -> int:
    args = parse_args()
    nks = [9, 11, 13]
    data = load_grid(nks)
    mus = [-4.0, 0.0, 2.0, 4.0]
    colors = {
        -4.0: "#1f77b4",
        0.0: "#2ca02c",
        2.0: "#9467bd",
        4.0: "#d62728",
    }
    panels = [
        ("fixed_frobenius_norm", "fixed Frobenius norm"),
        ("fixed_delta0", r"fixed $\Delta_0$"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.8), sharex=True)
    for axis, (normalization, title) in zip(axes, panels):
        axis.axhline(0.0, color="#555555", linewidth=0.9, linestyle="--")
        for mu in mus:
            values = [data[(normalization, mu)][nk] for nk in nks]
            axis.plot(
                nks,
                values,
                marker="o",
                linewidth=1.8,
                color=colors[mu],
                label=fr"$\mu={mu:g}$ meV",
            )
        axis.set_title(title)
        axis.set_xlabel(r"$nk$")
        axis.set_xticks(nks)
        axis.set_ylabel(r"$100[D_{\rm iso}(1)/D_{\rm iso}(0)-1]$")
        axis.grid(True, alpha=0.25)
        axis.legend(frameon=False, fontsize=8)

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=200)
    pdf_output = args.output.with_suffix(".pdf")
    fig.savefig(pdf_output)
    print(f"Wrote {args.output}")
    print(f"Wrote {pdf_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
