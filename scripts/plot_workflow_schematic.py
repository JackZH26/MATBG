#!/usr/bin/env python3
"""Draw the manuscript workflow schematic."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "figures" / "workflow_schematic_prb.png",
    )
    return parser.parse_args()


def add_box(
    axis: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    title: str,
    body: str,
    facecolor: str,
) -> None:
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.018,rounding_size=0.025",
        linewidth=1.15,
        edgecolor="#24364b",
        facecolor=facecolor,
    )
    axis.add_patch(box)
    x, y = xy
    axis.text(
        x + 0.04 * width,
        y + 0.72 * height,
        title,
        ha="left",
        va="center",
        fontsize=10.8,
        fontweight="bold",
        color="#132235",
    )
    axis.text(
        x + 0.04 * width,
        y + 0.36 * height,
        body,
        ha="left",
        va="center",
        fontsize=9.2,
        color="#1f2937",
        linespacing=1.25,
    )


def add_arrow(axis: plt.Axes, start: tuple[float, float], end: tuple[float, float]) -> None:
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=14,
        linewidth=1.4,
        color="#415a77",
        shrinkA=5,
        shrinkB=5,
    )
    axis.add_patch(arrow)


def main() -> int:
    args = parse_args()

    fig, axis = plt.subplots(figsize=(12.4, 4.7), constrained_layout=True)
    axis.set_xlim(-0.01, 1.02)
    axis.set_ylim(0, 1)
    axis.axis("off")

    boxes = [
        (
            "BM normal state",
            r"$H_{\rm BM}(\mathbf{k})$" + "\n" + r"$n_{\rm keep}=6$ bands",
            "#e9f1fb",
        ),
        (
            "Orbital gap direction",
            r"$\Delta_{\rm orb}=\Delta_0{\cal N}_{\eta}(M_0+\eta M_1)$"
            + "\n"
            + r"$M_1=\tau_x\sigma_x$",
            "#ecf7ef",
        ),
        (
            "TR-sewn projection",
            r"$\Delta_{\rm band}=U_+^\dagger\Delta_{\rm orb}U_+$"
            + "\n"
            + r"$W_{\rm inter}$ diagnostic",
            "#fff5df",
        ),
        (
            "Finite-band BdG",
            r"$H_{\rm BdG}(\mathbf{k})$ response"
            + "\n"
            + r"$D_{\rm iso}=(D_{xx}+D_{yy})/2$",
            "#f2ecfb",
        ),
        (
            "Claim-bearing map",
            r"$D_{\rm iso}(\mu,\eta)/D_{\rm iso}(\mu,0)-1$"
            + "\n"
            + r"Frobenius vs. fixed $\Delta_0$",
            "#fdeeee",
        ),
    ]

    x0 = 0.025
    y0 = 0.38
    width = 0.165
    height = 0.36
    gap = 0.035
    centers: list[tuple[float, float]] = []
    for index, (title, body, facecolor) in enumerate(boxes):
        x = x0 + index * (width + gap)
        add_box(axis, (x, y0), width, height, title, body, facecolor)
        centers.append((x + width, y0 + 0.5 * height))
        if index > 0:
            previous = x0 + (index - 1) * (width + gap) + width
            add_arrow(axis, (previous, y0 + 0.5 * height), (x, y0 + 0.5 * height))

    banner = FancyBboxPatch(
        (0.08, 0.12),
        0.84,
        0.14,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=1.05,
        edgecolor="#6b7280",
        facecolor="#f8fafc",
    )
    axis.add_patch(banner)
    axis.text(
        0.5,
        0.19,
        "Self-audit boundary: normalized ratios carry the mechanism claim; "
        "raw eV A$^2$ values and filling proxies remain benchmark controls.",
        ha="center",
        va="center",
        fontsize=10.0,
        color="#24364b",
    )

    axis.text(
        0.5,
        0.9,
        "Executable route from orbital pairing structure to a normalized MATBG response signature",
        ha="center",
        va="center",
        fontsize=12.5,
        fontweight="bold",
        color="#111827",
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=220)
    pdf_output = args.output.with_suffix(".pdf")
    fig.savefig(pdf_output)
    print(f"Wrote {args.output}")
    print(f"Wrote {pdf_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
