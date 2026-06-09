#!/usr/bin/env python3
"""Summarize eta-target response relative to an eta-baseline scan."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output CSV path. Defaults to INPUT stem plus _eta_summary.csv.",
    )
    parser.add_argument("--eta-baseline", type=float, default=0.0)
    parser.add_argument("--eta-target", type=float, default=1.0)
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(row: dict[str, str], key: str, default: float = float("nan")) -> float:
    if key not in row or row[key] == "":
        return default
    return float(row[key])


def d_iso(row: dict[str, str]) -> float:
    if "D_iso_raw" in row and row["D_iso_raw"]:
        return float(row["D_iso_raw"])
    return 0.5 * (float(row["Dxx_total_raw"]) + float(row["Dyy_total_raw"]))


def geom_fraction(row: dict[str, str]) -> float:
    if "geom_fraction_total" in row and row["geom_fraction_total"]:
        return float(row["geom_fraction_total"])
    geom = float(row["Dxx_geom_raw"]) + float(row["Dyy_geom_raw"])
    total = float(row["Dxx_total_raw"]) + float(row["Dyy_total_raw"])
    return geom / total if total else float("nan")


def row_key(row: dict[str, str]) -> tuple[str, float]:
    return row["normalization"], float(row["mu_meV"])


def output_path(args: argparse.Namespace) -> Path:
    if args.output is not None:
        return args.output
    return args.input.with_name(f"{args.input.stem}_eta_summary.csv")


def main() -> int:
    args = parse_args()
    rows = load_rows(args.input)
    baseline: dict[tuple[str, float], dict[str, str]] = {}
    target: dict[tuple[str, float], dict[str, str]] = {}

    for row in rows:
        eta = float(row["eta"])
        if abs(eta - args.eta_baseline) < 1.0e-12:
            baseline[row_key(row)] = row
        if abs(eta - args.eta_target) < 1.0e-12:
            target[row_key(row)] = row

    fieldnames = [
        "normalization",
        "mu_meV",
        "nu_proxy",
        "eta_baseline",
        "eta_target",
        "D_iso_baseline",
        "D_iso_target",
        "D_iso_rel_target_vs_baseline",
        "geom_fraction_baseline",
        "geom_fraction_target",
        "geom_fraction_delta_target_vs_baseline",
        "anisotropy_ratio_baseline",
        "anisotropy_ratio_target",
        "W_inter_baseline",
        "W_inter_target",
    ]

    summary_rows: list[dict[str, object]] = []
    for key in sorted(set(baseline).intersection(target), key=lambda item: (item[0], item[1])):
        base = baseline[key]
        targ = target[key]
        base_d = d_iso(base)
        target_d = d_iso(targ)
        base_geom = geom_fraction(base)
        target_geom = geom_fraction(targ)
        summary_rows.append(
            {
                "normalization": key[0],
                "mu_meV": key[1],
                "nu_proxy": as_float(targ, "nu_proxy", as_float(base, "nu_proxy")),
                "eta_baseline": args.eta_baseline,
                "eta_target": args.eta_target,
                "D_iso_baseline": base_d,
                "D_iso_target": target_d,
                "D_iso_rel_target_vs_baseline": target_d / base_d - 1.0,
                "geom_fraction_baseline": base_geom,
                "geom_fraction_target": target_geom,
                "geom_fraction_delta_target_vs_baseline": target_geom - base_geom,
                "anisotropy_ratio_baseline": as_float(base, "anisotropy_ratio"),
                "anisotropy_ratio_target": as_float(targ, "anisotropy_ratio"),
                "W_inter_baseline": as_float(base, "interband_pairing_weight_mean"),
                "W_inter_target": as_float(targ, "interband_pairing_weight_mean"),
            }
        )

    out = output_path(args)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(summary_rows)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
