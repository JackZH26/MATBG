#!/usr/bin/env python3
"""Audit valley-sewing response sensitivity for the PRB major revision."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = ROOT / "data" / "processed" / "valley_sewing_response_sensitivity_summary.csv"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "valley_sewing_response_sensitivity_audit.csv"


EXPECTED_PARTNERS = {
    "tr_sewn",
    "same_valley",
    "time_reversed_valley",
    "sewn_time_reversed_valley",
}


@dataclass(frozen=True)
class AuditRow:
    check_id: str
    status: str
    measured_value: str
    criterion: str
    interpretation: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def add(
    rows: list[AuditRow],
    check_id: str,
    ok: bool,
    measured_value: str,
    criterion: str,
    interpretation: str,
) -> None:
    rows.append(
        AuditRow(
            check_id=check_id,
            status="pass" if ok else "fail",
            measured_value=measured_value,
            criterion=criterion,
            interpretation=interpretation,
        )
    )


def values(rows: list[dict[str, str]], key: str) -> list[float]:
    return [float(row[key]) for row in rows]


def main() -> int:
    args = parse_args()
    rows = load_csv(args.summary)
    audit: list[AuditRow] = []

    partners = {row["partner"] for row in rows}
    nks = sorted({int(row["nk"]) for row in rows})
    n_shells = sorted({int(row["n_shell"]) for row in rows})
    mus = sorted({float(row["mu_meV"]) for row in rows})
    normalizations = sorted({row["normalization"] for row in rows})
    tr_frob = [
        row
        for row in rows
        if row["partner"] == "tr_sewn" and row["normalization"] == "fixed_frobenius_norm"
    ]
    alternative_frob = [
        row
        for row in rows
        if row["partner"] != "tr_sewn" and row["normalization"] == "fixed_frobenius_norm"
    ]
    all_frob = [row for row in rows if row["normalization"] == "fixed_frobenius_norm"]
    tr_rows = [row for row in rows if row["partner"] == "tr_sewn"]
    alternative_rows = [row for row in rows if row["partner"] != "tr_sewn"]

    grouped: dict[tuple[int, int, int, float, str], list[float]] = defaultdict(list)
    for row in all_frob:
        grouped[
            (
                int(row["nk"]),
                int(row["n_keep"]),
                int(row["n_shell"]),
                float(row["mu_meV"]),
                row["normalization"],
            )
        ].append(float(row["D_iso_rel_percent"]))
    partner_spreads = [max(items) - min(items) for items in grouped.values()]

    add(
        audit,
        "partner_coverage",
        partners == EXPECTED_PARTNERS,
        ",".join(sorted(partners)),
        "all four valley-partner conventions are present",
        "The response sensitivity test covers the working convention and three alternatives.",
    )
    add(
        audit,
        "axis_coverage",
        nks == [9, 13, 15] and n_shells == [3, 4] and mus == [-4.0, 0.0, 2.0, 4.0],
        f"nks={nks}; n_shells={n_shells}; mus={mus}; normalizations={normalizations}",
        "key-point response sensitivity covers the planned axes",
        "The test samples production grids and shell cutoffs without becoming a dense rerun.",
    )
    add(
        audit,
        "tr_sewn_reference_positive",
        all(value > 0.0 for value in values(tr_frob, "D_iso_rel_percent")),
        f"{sum(value > 0.0 for value in values(tr_frob, 'D_iso_rel_percent'))}/{len(tr_frob)} positive",
        "the working tr_sewn reference remains positive",
        "The sensitivity study reproduces the production-scope positive sign.",
    )
    add(
        audit,
        "alternative_partner_sign_sensitivity_detected",
        any(value <= 0.0 for value in values(alternative_frob, "D_iso_rel_percent")),
        f"{sum(value > 0.0 for value in values(alternative_frob, 'D_iso_rel_percent'))}/{len(alternative_frob)} positive",
        "at least one alternative partner convention changes the fixed-Frobenius sign",
        "The revision must not present the response as valley-sewing independent.",
    )
    add(
        audit,
        "partner_sensitivity_quantified",
        bool(partner_spreads),
        f"max_spread={max(partner_spreads):.3f} percentage points; mean_spread={sum(partner_spreads)/len(partner_spreads):.3f}",
        "partner-convention spread is explicitly measured",
        "The revision can discuss valley-sewing sensitivity quantitatively rather than as a vague caveat.",
    )
    add(
        audit,
        "sewing_alignment_recorded",
        max(values(rows, "raw_partner_alignment_error_mean")) > 0.0
        and min(values(rows, "partner_min_singular_value_min")) >= 0.0,
        f"max_raw_alignment={max(values(rows, 'raw_partner_alignment_error_mean')):.3e}; min_sv={min(values(rows, 'partner_min_singular_value_min')):.3e}",
        "partner alignment diagnostics are recorded",
        "The response sensitivity table includes evidence for how far raw partners are from the TR target.",
    )
    add(
        audit,
        "tr_sewn_numerical_error_bounds",
        max(values(tr_rows, "max_ph_spectrum_error")) < 1.0e-8,
        f"max_ph={max(values(tr_rows, 'max_ph_spectrum_error')):.3e}",
        "working tr_sewn particle-hole spectrum error remains below 1e-8",
        "The production convention remains numerically PH-consistent.",
    )
    add(
        audit,
        "alternative_partner_ph_sensitivity_recorded",
        max(values(alternative_rows, "max_ph_spectrum_error")) > 1.0e-4,
        f"max_ph={max(values(alternative_rows, 'max_ph_spectrum_error')):.3e}",
        "alternative partner conventions show measurable PH-spectrum sensitivity",
        "Alternative partners are diagnostic stress tests rather than replacement production conventions.",
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "check_id",
                "status",
                "measured_value",
                "criterion",
                "interpretation",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows([row.__dict__ for row in audit])

    pass_count = sum(row.status == "pass" for row in audit)
    print(f"Wrote {args.output}")
    print(f"Valley-sewing response sensitivity checks passed: {pass_count}/{len(audit)}")
    failures = [row for row in audit if row.status != "pass"]
    if failures:
        for row in failures:
            print(f"FAIL: {row.check_id}: {row.measured_value}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
