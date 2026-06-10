#!/usr/bin/env python3
"""Audit first-pass pairing-family response evidence for major revision."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = ROOT / "data" / "processed" / "pairing_family_response_summary.csv"
DEFAULT_RAW = ROOT / "data" / "processed" / "pairing_family_response_scan.csv"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "pairing_family_response_audit.csv"


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
    parser.add_argument("--raw", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def status(ok: bool) -> str:
    return "pass" if ok else "fail"


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
            status=status(ok),
            measured_value=measured_value,
            criterion=criterion,
            interpretation=interpretation,
        )
    )


def values(rows: list[dict[str, str]], column: str) -> list[float]:
    return [float(row[column]) for row in rows]


def main() -> int:
    args = parse_args()
    summary_rows = load_csv(args.summary)
    raw_rows = load_csv(args.raw)
    audit: list[AuditRow] = []

    directions = sorted({row["m1"] for row in summary_rows})
    frob_rows = [
        row for row in summary_rows if row["normalization"] == "fixed_frobenius_norm"
    ]
    delta_rows = [row for row in summary_rows if row["normalization"] == "fixed_delta0"]
    frob_pct = values(frob_rows, "D_iso_rel_percent")
    delta_pct = values(delta_rows, "D_iso_rel_percent")
    raw_matrix_flags = {
        (row["matrix_real"], row["matrix_symmetric"], row["matrix_hermitian"])
        for row in raw_rows
    }

    add(
        audit,
        "candidate_direction_count",
        len(directions) >= 8,
        str(len(directions)),
        "at least eight real layer-sublattice directions are scanned",
        "The first major-revision family scan is broader than one ansatz.",
    )
    add(
        audit,
        "candidate_matrix_flags",
        raw_matrix_flags == {("True", "True", "True")},
        str(sorted(raw_matrix_flags)),
        "all scanned matrices are real, symmetric, and Hermitian",
        "The current candidate family stays within the intended real even-parity test set.",
    )
    add(
        audit,
        "working_direction_included",
        "taux_sigmax" in directions,
        ",".join(directions),
        "the original M1=taux_sigmax direction is included",
        "The family scan can be compared directly with the current manuscript result.",
    )
    add(
        audit,
        "fixed_frobenius_all_positive",
        all(value > 0.0 for value in frob_pct),
        f"{sum(value > 0.0 for value in frob_pct)}/{len(frob_pct)} rows positive",
        "all fixed-Frobenius eta=1 rows are positive",
        "The positive normalized signature is not unique to the original direction at this grid.",
    )
    add(
        audit,
        "fixed_frobenius_minimum_size",
        min(frob_pct) > 5.0,
        f"min={min(frob_pct):.3f}%, max={max(frob_pct):.3f}%",
        "minimum fixed-Frobenius response exceeds five percent in the first-pass family scan",
        "The family response has comparable scale to the manuscript's main diagnostic.",
    )
    add(
        audit,
        "fixed_delta0_has_sign_sensitivity",
        min(delta_pct) < 0.0 < max(delta_pct),
        f"min={min(delta_pct):.3f}%, max={max(delta_pct):.3f}%",
        "fixed-Delta0 control includes both signs",
        "The normalization dependence remains central and cannot be hidden in the revision.",
    )
    add(
        audit,
        "fixed_delta0_weaker_than_frobenius",
        max(abs(value) for value in delta_pct) < 0.5 * min(frob_pct),
        f"max_abs_delta0={max(abs(value) for value in delta_pct):.3f}%, min_frob={min(frob_pct):.3f}%",
        "fixed-Delta0 absolute response is less than half the weakest fixed-Frobenius response",
        "The control remains substantially weaker than the normalized family response.",
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
    print(f"Pairing-family response checks passed: {pass_count}/{len(audit)}")
    failures = [row for row in audit if row.status != "pass"]
    if failures:
        for row in failures:
            print(f"FAIL: {row.check_id}: {row.measured_value}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
