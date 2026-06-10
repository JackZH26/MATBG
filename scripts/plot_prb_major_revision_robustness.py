#!/usr/bin/env python3
"""Plot the major-revision grid/truncation/shell robustness matrix."""

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
        default=ROOT / "data" / "processed" / "prb_major_revision_robustness_summary.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "figures" / "prb_major_revision_robustness_matrix.png",
    )
    parser.add_argument(
        "--pdf-output",
        type=Path,
        default=ROOT / "figures" / "prb_major_revision_robustness_matrix.pdf",
    )
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    args = parse_args()
    rows = [
        row
        for row in load_rows(args.input)
        if row["normalization"] == "fixed_frobenius_norm"
    ]
    n_shells = sorted({int(row["n_shell"]) for row in rows})
    n_keeps = sorted({int(row["n_keep"]) for row in rows})
    mus = sorted({float(row["mu_meV"]) for row in rows})
    colors = plt.cm.viridis(np.linspace(0.08, 0.9, len(mus)))
    color_by_mu = dict(zip(mus, colors))

    grouped: dict[tuple[int, int, float], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(int(row["n_shell"]), int(row["n_keep"]), float(row["mu_meV"]))].append(row)

    fig, axes = plt.subplots(
        len(n_shells),
        len(n_keeps),
        figsize=(10.5, 7.5),
        sharex=True,
        sharey=True,
    )
    for row_index, n_shell in enumerate(n_shells):
        for col_index, n_keep in enumerate(n_keeps):
            axis = axes[row_index][col_index]
            axis.axhline(0.0, color="black", linewidth=0.8)
            for mu in mus:
                subset = sorted(
                    grouped[(n_shell, n_keep, mu)],
                    key=lambda item: int(item["nk"]),
                )
                nks = [int(item["nk"]) for item in subset]
                values = [float(item["D_iso_rel_percent"]) for item in subset]
                axis.plot(
                    nks,
                    values,
                    marker="o",
                    markersize=3.5,
                    linewidth=1.0,
                    color=color_by_mu[mu],
                    label=f"{mu:g} meV" if row_index == 0 and col_index == 0 else None,
                )
            axis.set_title(f"n_shell={n_shell}, n_keep={n_keep}", fontsize=10)
            axis.grid(alpha=0.25, linewidth=0.6)
            if row_index == len(n_shells) - 1:
                axis.set_xlabel("nk")
            if col_index == 0:
                axis.set_ylabel(r"$100[D_{\rm iso}(1)/D_{\rm iso}(0)-1]$")

    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.suptitle(
        "Major-revision robustness matrix for fixed-Frobenius response",
        y=0.985,
    )
    fig.legend(
        handles,
        labels,
        loc="lower center",
        ncols=len(mus),
        frameon=False,
        bbox_to_anchor=(0.5, 0.005),
    )
    fig.tight_layout(rect=(0.0, 0.06, 1.0, 0.95))

    for path in (args.output, args.pdf_output):
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=200)
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
