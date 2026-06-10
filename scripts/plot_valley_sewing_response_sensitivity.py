#!/usr/bin/env python3
"""Plot response sensitivity to valley partner/sewing conventions."""

from __future__ import annotations

import argparse
import csv
import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "matplotlib-matbg"))
os.environ.setdefault("XDG_CACHE_HOME", str(Path(tempfile.gettempdir()) / "fontcache-matbg"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PARTNER_ORDER = [
    "tr_sewn",
    "same_valley",
    "time_reversed_valley",
    "sewn_time_reversed_valley",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "data" / "processed" / "valley_sewing_response_sensitivity_summary.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "figures" / "valley_sewing_response_sensitivity.png",
    )
    parser.add_argument(
        "--pdf-output",
        type=Path,
        default=ROOT / "figures" / "valley_sewing_response_sensitivity.pdf",
    )
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def partner_label(partner: str) -> str:
    return partner.replace("_", "\n")


def main() -> int:
    args = parse_args()
    rows = [
        row
        for row in load_rows(args.input)
        if row["normalization"] == "fixed_frobenius_norm"
    ]
    fig, (ax_response, ax_ph) = plt.subplots(
        2,
        1,
        figsize=(8.0, 6.0),
        sharex=True,
        gridspec_kw={"height_ratios": [2.2, 1.0]},
    )
    x_positions = np.arange(len(PARTNER_ORDER))
    colors = ["#1f77b4", "#9467bd", "#b45f06", "#2ca02c"]

    for index, partner in enumerate(PARTNER_ORDER):
        partner_rows = [row for row in rows if row["partner"] == partner]
        response = np.asarray(
            [float(row["D_iso_rel_percent"]) for row in partner_rows],
            dtype=float,
        )
        ph_error = np.asarray(
            [float(row["max_ph_spectrum_error"]) for row in partner_rows],
            dtype=float,
        )
        jitter = np.linspace(-0.16, 0.16, len(response))
        ax_response.scatter(
            x_positions[index] + jitter,
            response,
            s=24,
            color=colors[index],
            alpha=0.75,
            edgecolor="none",
        )
        ax_response.errorbar(
            x_positions[index],
            float(np.mean(response)),
            yerr=[
                [float(np.mean(response) - np.min(response))],
                [float(np.max(response) - np.mean(response))],
            ],
            fmt="o",
            color="black",
            capsize=4,
            markersize=5,
        )
        ax_ph.bar(
            x_positions[index],
            float(np.max(ph_error)),
            width=0.55,
            color=colors[index],
            alpha=0.8,
        )

    ax_response.axhline(0.0, color="black", linewidth=0.8)
    ax_response.set_ylabel(r"$100[D_{\rm iso}(1)/D_{\rm iso}(0)-1]$")
    ax_response.set_title("Valley-partner sensitivity of fixed-Frobenius response")
    ax_response.grid(axis="y", alpha=0.25)
    ax_ph.set_yscale("symlog", linthresh=1.0e-10)
    ax_ph.set_ylabel("max PH\nerror")
    ax_ph.grid(axis="y", alpha=0.25)
    ax_ph.set_xticks(x_positions)
    ax_ph.set_xticklabels([partner_label(partner) for partner in PARTNER_ORDER])
    ax_ph.set_xlabel("paired-sector convention")
    fig.tight_layout()

    for path in (args.output, args.pdf_output):
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=200)
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
