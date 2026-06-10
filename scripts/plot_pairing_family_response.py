#!/usr/bin/env python3
"""Plot the first-pass pairing-family response summary."""

from __future__ import annotations

import argparse
import csv
import os
import tempfile
from collections import defaultdict
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "matplotlib-matbg"))
os.environ.setdefault("XDG_CACHE_HOME", str(Path(tempfile.gettempdir()) / "fontcache-matbg"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "data" / "processed" / "pairing_family_response_summary.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "figures" / "pairing_family_response_summary.png",
    )
    parser.add_argument(
        "--pdf-output",
        type=Path,
        default=ROOT / "figures" / "pairing_family_response_summary.pdf",
    )
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def grouped(rows: list[dict[str, str]]) -> dict[tuple[str, str], list[dict[str, str]]]:
    data: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        data[(row["m1"], row["normalization"])].append(row)
    return data


def values(rows: list[dict[str, str]], column: str) -> np.ndarray:
    return np.asarray([float(row[column]) for row in rows], dtype=float)


def main() -> int:
    args = parse_args()
    rows = load_rows(args.input)
    data = grouped(rows)
    directions = sorted({row["m1"] for row in rows})
    labels = [item.replace("_", r"\_") for item in directions]
    x = np.arange(len(directions))

    fig, (ax_resp, ax_weight) = plt.subplots(
        2,
        1,
        figsize=(8.0, 6.2),
        sharex=True,
        gridspec_kw={"height_ratios": [2.2, 1.0]},
        constrained_layout=True,
    )

    styles = {
        "fixed_frobenius_norm": {
            "offset": -0.13,
            "label": "fixed Frobenius",
            "color": "#1f77b4",
        },
        "fixed_delta0": {
            "offset": 0.13,
            "label": r"fixed $\Delta_0$",
            "color": "#b45f06",
        },
    }
    for normalization, style in styles.items():
        means: list[float] = []
        lower: list[float] = []
        upper: list[float] = []
        for direction in directions:
            pct = values(data[(direction, normalization)], "D_iso_rel_percent")
            mean = float(np.mean(pct))
            means.append(mean)
            lower.append(mean - float(np.min(pct)))
            upper.append(float(np.max(pct)) - mean)
        ax_resp.errorbar(
            x + style["offset"],
            means,
            yerr=[lower, upper],
            fmt="o",
            markersize=5,
            capsize=3,
            color=style["color"],
            label=style["label"],
        )

    weights = [
        float(np.mean(values(data[(direction, "fixed_frobenius_norm")], "W_inter_target")))
        for direction in directions
    ]
    ax_weight.bar(x, weights, color="#4c7c59", width=0.62)
    ax_resp.axhline(0.0, color="black", linewidth=0.8)
    ax_resp.set_ylabel(r"$100[D_{\rm iso}(\eta=1)/D_{\rm iso}(0)-1]$")
    ax_resp.legend(frameon=False, ncols=2)
    ax_resp.set_title("Pairing-family response at nk=7, n_keep=6, n_shell=3")
    ax_weight.set_ylabel(r"$W_{\rm inter}$")
    ax_weight.set_xticks(x)
    ax_weight.set_xticklabels(labels, rotation=35, ha="right")
    ax_weight.set_xlabel(r"orbital direction $M_1$")

    for path in (args.output, args.pdf_output):
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=200)
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
