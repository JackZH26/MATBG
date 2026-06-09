#!/usr/bin/env python3
"""Append conservative unit-conversion columns to response CSV files."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from matbg.units import (  # noqa: E402
    DEFAULT_SPIN_VALLEY_DEGENERACY,
    ev_a2_to_cell_kelvin,
    moire_cell_area_angstrom2,
    moire_reciprocal_scale_angstrom_inv,
    raw_mev_a2_to_ev_a2,
)


RAW_COMPONENTS = [
    "D_iso_raw",
    "Dxx_total_raw",
    "Dxx_conv_raw",
    "Dxx_geom_raw",
    "Dxx_cross_raw",
    "Dyy_total_raw",
    "Dyy_conv_raw",
    "Dyy_geom_raw",
    "Dyy_cross_raw",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--theta-deg", type=float, default=1.05)
    parser.add_argument(
        "--spin-valley-degeneracy",
        type=float,
        default=DEFAULT_SPIN_VALLEY_DEGENERACY,
    )
    return parser.parse_args()


def load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def value(row: dict[str, str], key: str) -> float | None:
    if key not in row or row[key] == "":
        return None
    return float(row[key])


def d_iso(row: dict[str, str]) -> float | None:
    explicit = value(row, "D_iso_raw")
    if explicit is not None:
        return explicit
    dxx = value(row, "Dxx_total_raw")
    dyy = value(row, "Dyy_total_raw")
    if dxx is None or dyy is None:
        return None
    return 0.5 * (dxx + dyy)


def converted_fields(fieldnames: list[str]) -> list[str]:
    fields = [
        "theta_deg",
        "moire_cell_area_A2",
        "moire_reciprocal_scale_Ainv",
    ]
    for component in RAW_COMPONENTS:
        raw_name = component.removesuffix("_raw")
        if component == "D_iso_raw" or component in fieldnames:
            fields.extend(
                [
                    f"{raw_name}_eV_A2_per_flavor",
                    f"{raw_name}_eV_A2_spin_valley",
                    f"{raw_name}_cell_K_per_flavor",
                    f"{raw_name}_cell_K_spin_valley",
                ]
            )
    return fields


def add_conversions(
    row: dict[str, str],
    fieldnames: list[str],
    theta_deg: float,
    degeneracy: float,
) -> dict[str, object]:
    output: dict[str, object] = dict(row)
    area = moire_cell_area_angstrom2(theta_deg)
    output["theta_deg"] = theta_deg
    output["moire_cell_area_A2"] = area
    output["moire_reciprocal_scale_Ainv"] = moire_reciprocal_scale_angstrom_inv(theta_deg)

    for component in RAW_COMPONENTS:
        raw = d_iso(row) if component == "D_iso_raw" else value(row, component)
        if raw is None:
            continue
        raw_name = component.removesuffix("_raw")
        per_flavor = raw_mev_a2_to_ev_a2(raw)
        spin_valley = raw_mev_a2_to_ev_a2(raw, degeneracy=degeneracy)
        if component == "D_iso_raw" or component in fieldnames:
            output[f"{raw_name}_eV_A2_per_flavor"] = per_flavor
            output[f"{raw_name}_eV_A2_spin_valley"] = spin_valley
            output[f"{raw_name}_cell_K_per_flavor"] = ev_a2_to_cell_kelvin(
                per_flavor,
                theta_deg,
            )
            output[f"{raw_name}_cell_K_spin_valley"] = ev_a2_to_cell_kelvin(
                spin_valley,
                theta_deg,
            )
    return output


def main() -> int:
    args = parse_args()
    fieldnames, rows = load_rows(args.input)
    extra_fields = [field for field in converted_fields(fieldnames) if field not in fieldnames]
    output_rows = [
        add_conversions(
            row,
            fieldnames=fieldnames,
            theta_deg=args.theta_deg,
            degeneracy=args.spin_valley_degeneracy,
        )
        for row in rows
    ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames + extra_fields)
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
