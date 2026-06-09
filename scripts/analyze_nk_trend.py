#!/usr/bin/env python3
"""Finite-grid trend audit for selected nk convergence key points."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nks", type=int, nargs="+", default=[9, 11, 13])
    parser.add_argument("--mus", type=float, nargs="+", default=[-4.0, 0.0, 2.0, 4.0])
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=ROOT / "data" / "processed" / "nk_trend_audit_nkeep6.csv",
    )
    parser.add_argument(
        "--figure-output",
        type=Path,
        default=ROOT / "figures" / "nk_trend_audit_nkeep6.png",
    )
    return parser.parse_args()


def summary_path(nk: int) -> Path:
    return (
        ROOT
        / "data"
        / "processed"
        / f"mu_response_scan_nk{nk}_nkeep6_keypoints_summary.csv"
    )


def load_values(nks: list[int]) -> dict[tuple[str, float], dict[int, float]]:
    data: dict[tuple[str, float], dict[int, float]] = {}
    for nk in nks:
        with summary_path(nk).open(newline="") as handle:
            for row in csv.DictReader(handle):
                key = (row["normalization"], float(row["mu_meV"]))
                data.setdefault(key, {})[nk] = (
                    100.0 * float(row["D_iso_rel_target_vs_baseline"])
                )
    return data


def linear_fit(nks: list[int], values: list[float], power: int) -> dict[str, float]:
    x = np.asarray([1.0 / (nk**power) for nk in nks], dtype=float)
    y = np.asarray(values, dtype=float)
    design = np.column_stack([np.ones_like(x), x])
    intercept, slope = np.linalg.lstsq(design, y, rcond=None)[0]
    fitted = design @ np.asarray([intercept, slope])
    rms = float(np.sqrt(np.mean((y - fitted) ** 2)))
    return {
        "intercept": float(intercept),
        "slope": float(slope),
        "rms": rms,
    }


def sign_status(values: list[float]) -> str:
    if all(value > 0.0 for value in values):
        return "positive"
    if all(value < 0.0 for value in values):
        return "negative"
    return "mixed"


def build_rows(
    data: dict[tuple[str, float], dict[int, float]],
    nks: list[int],
    mus: list[float],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for normalization in ("fixed_delta0", "fixed_frobenius_norm"):
        for mu in mus:
            values = [data[(normalization, mu)][nk] for nk in nks]
            fit_h1 = linear_fit(nks, values, power=1)
            fit_h2 = linear_fit(nks, values, power=2)
            rows.append(
                {
                    "normalization": normalization,
                    "mu_meV": mu,
                    "nk9_percent": values[nks.index(9)] if 9 in nks else "",
                    "nk11_percent": values[nks.index(11)] if 11 in nks else "",
                    "nk13_percent": values[nks.index(13)] if 13 in nks else "",
                    "min_percent": min(values),
                    "max_percent": max(values),
                    "delta_13_minus_9_percent": (
                        data[(normalization, mu)][13] - data[(normalization, mu)][9]
                        if 9 in nks and 13 in nks
                        else ""
                    ),
                    "measured_sign_status": sign_status(values),
                    "intercept_percent_h2": fit_h2["intercept"],
                    "rms_percent_h2": fit_h2["rms"],
                    "intercept_percent_h1": fit_h1["intercept"],
                    "rms_percent_h1": fit_h1["rms"],
                    "intercept_spread_percent": abs(
                        fit_h2["intercept"] - fit_h1["intercept"]
                    ),
                    "intercepts_positive": (
                        "yes"
                        if fit_h1["intercept"] > 0.0 and fit_h2["intercept"] > 0.0
                        else "no"
                    ),
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0].keys()),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def plot_trend(
    path: Path,
    data: dict[tuple[str, float], dict[int, float]],
    nks: list[int],
    mus: list[float],
) -> None:
    colors = {
        -4.0: "#1f77b4",
        0.0: "#2ca02c",
        2.0: "#9467bd",
        4.0: "#d62728",
    }
    panels = [
        ("fixed_frobenius_norm", "fixed Frobenius norm"),
        ("fixed_delta0", r"fixed $\Delta_0$ control"),
    ]
    x = np.asarray([1.0 / (nk**2) for nk in nks], dtype=float)
    x_line = np.linspace(0.0, float(np.max(x)), 100)

    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.8), sharey=False)
    for axis, (normalization, title) in zip(axes, panels):
        axis.axhline(0.0, color="#555555", linewidth=0.9, linestyle="--")
        for mu in mus:
            values = [data[(normalization, mu)][nk] for nk in nks]
            fit = linear_fit(nks, values, power=2)
            y_line = fit["intercept"] + fit["slope"] * x_line
            axis.plot(
                x_line,
                y_line,
                linewidth=1.1,
                linestyle=":",
                color=colors[mu],
                alpha=0.8,
            )
            axis.plot(
                x,
                values,
                marker="o",
                linewidth=0.0,
                color=colors[mu],
                label=fr"$\mu={mu:g}$ meV",
            )
            axis.plot(
                [0.0],
                [fit["intercept"]],
                marker="x",
                color=colors[mu],
                markersize=6,
            )
        axis.set_title(title)
        axis.set_xlabel(r"$1/nk^2$")
        axis.set_ylabel(r"$100[D_{\rm iso}(1)/D_{\rm iso}(0)-1]$")
        axis.grid(True, alpha=0.25)
        axis.set_xticks([0.0, 1.0 / 13**2, 1.0 / 11**2, 1.0 / 9**2])
        axis.set_xticklabels(["0", r"$13^{-2}$", r"$11^{-2}$", r"$9^{-2}$"])
        axis.legend(frameon=False, fontsize=8)

    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200)
    fig.savefig(path.with_suffix(".pdf"))
    plt.close(fig)


def main() -> int:
    args = parse_args()
    nks = sorted(args.nks)
    data = load_values(nks)
    rows = build_rows(data, nks=nks, mus=args.mus)
    write_csv(args.csv_output, rows)
    plot_trend(args.figure_output, data=data, nks=nks, mus=args.mus)

    print(f"Wrote {args.csv_output}")
    print(f"Wrote {args.figure_output}")
    print(f"Wrote {args.figure_output.with_suffix('.pdf')}")
    print("normalization mu measured_sign h2_intercept h1_intercept")
    for row in rows:
        print(
            f"{str(row['normalization']):22s} "
            f"{float(row['mu_meV']):5.1f} "
            f"{str(row['measured_sign_status']):8s} "
            f"{float(row['intercept_percent_h2']):10.3f} "
            f"{float(row['intercept_percent_h1']):10.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
