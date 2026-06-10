#!/usr/bin/env python3
"""Audit grid/truncation/shell robustness evidence for the PRB revision."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "data" / "processed" / "prb_major_revision_robustness_matrix.csv"
DEFAULT_SUMMARY = ROOT / "data" / "processed" / "prb_major_revision_robustness_summary.csv"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "prb_major_revision_robustness_audit.csv"


@dataclass(frozen=True)
class AuditRow:
    check_id: str
    status: str
    measured_value: str
    criterion: str
    interpretation: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
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


def floats(rows: list[dict[str, str]], key: str) -> list[float]:
    return [float(row[key]) for row in rows]


def main() -> int:
    args = parse_args()
    matrix_rows = load_csv(args.matrix)
    summary_rows = load_csv(args.summary)
    audit: list[AuditRow] = []

    nks = sorted({int(row["nk"]) for row in summary_rows})
    n_keeps = sorted({int(row["n_keep"]) for row in summary_rows})
    n_shells = sorted({int(row["n_shell"]) for row in summary_rows})
    mus = sorted({float(row["mu_meV"]) for row in summary_rows})
    normalizations = sorted({row["normalization"] for row in summary_rows})
    raw_etas = sorted({float(row["eta"]) for row in matrix_rows})
    frob_rows = [
        row for row in summary_rows if row["normalization"] == "fixed_frobenius_norm"
    ]
    delta_rows = [row for row in summary_rows if row["normalization"] == "fixed_delta0"]
    frob_pct = floats(frob_rows, "D_iso_rel_percent")
    delta_pct = floats(delta_rows, "D_iso_rel_percent")
    frob_negative = [
        row for row in frob_rows if float(row["D_iso_rel_percent"]) <= 0.0
    ]
    frob_nkeep_ge6 = [row for row in frob_rows if int(row["n_keep"]) >= 6]
    frob_production_scope = [
        row
        for row in frob_rows
        if int(row["n_keep"]) >= 6 and int(row["n_shell"]) >= 3
    ]
    frob_nkeep_ge6_pct = floats(frob_nkeep_ge6, "D_iso_rel_percent")
    frob_production_pct = floats(frob_production_scope, "D_iso_rel_percent")
    expected_summary_rows = (
        len(nks) * len(n_keeps) * len(n_shells) * len(mus) * len(normalizations)
    )

    add(
        audit,
        "axis_nk_coverage",
        nks == [9, 11, 13, 15],
        str(nks),
        "nk coverage includes 9, 11, 13, and 15",
        "The revision directly extends the earlier selected-grid checks.",
    )
    add(
        audit,
        "axis_nkeep_coverage",
        n_keeps == [4, 6, 8],
        str(n_keeps),
        "retained-band coverage includes n_keep=4,6,8",
        "The result is tested against retained-band truncation.",
    )
    add(
        audit,
        "axis_nshell_coverage",
        n_shells == [2, 3, 4],
        str(n_shells),
        "moire shell coverage includes n_shell=2,3,4",
        "The result is tested against ultraviolet shell cutoff.",
    )
    add(
        audit,
        "axis_mu_coverage",
        mus == [-4.0, -2.0, 0.0, 2.0, 4.0],
        str(mus),
        "chemical-potential coverage includes -4,-2,0,2,4 meV",
        "The key response window is sampled beyond the previous four-point set.",
    )
    add(
        audit,
        "axis_eta_coverage",
        raw_etas == [0.0, 0.5, 1.0],
        str(raw_etas),
        "raw matrix includes eta=0,0.5,1",
        "The robustness matrix preserves the midpoint interpolation check.",
    )
    add(
        audit,
        "summary_row_count",
        len(summary_rows) == expected_summary_rows,
        f"{len(summary_rows)}/{expected_summary_rows}",
        "summary contains every nk/n_keep/n_shell/mu/normalization combination",
        "The audit is based on a complete rectangular robustness matrix.",
    )
    add(
        audit,
        "fixed_frobenius_claim_scope_positive",
        all(value > 0.0 for value in frob_nkeep_ge6_pct),
        f"{sum(value > 0.0 for value in frob_nkeep_ge6_pct)}/{len(frob_nkeep_ge6_pct)} positive",
        "all fixed-Frobenius eta=1 responses are positive for n_keep>=6",
        "The normalized response sign survives the production and expanded retained-band truncations.",
    )
    add(
        audit,
        "fixed_frobenius_production_scope_size",
        min(frob_production_pct) > 4.0,
        f"min={min(frob_production_pct):.3f}%, max={max(frob_production_pct):.3f}%",
        "minimum fixed-Frobenius response exceeds four percent for n_keep>=6 and n_shell>=3",
        "The production-scope response remains larger than a tiny numerical residual.",
    )
    add(
        audit,
        "fixed_frobenius_low_truncation_boundary",
        bool(frob_negative)
        and all(int(row["n_keep"]) == 4 and float(row["mu_meV"]) == -4.0 for row in frob_negative),
        f"{len(frob_negative)} nonpositive row(s): "
        + "; ".join(
            f"n_shell={row['n_shell']} nk={row['nk']} pct={float(row['D_iso_rel_percent']):.3f}%"
            for row in frob_negative[:8]
        ),
        "all nonpositive fixed-Frobenius rows are confined to n_keep=4 at mu=-4 meV",
        "The revision must state that the signal is not globally truncation-independent at the lowest retained-band cutoff.",
    )
    add(
        audit,
        "fixed_frobenius_production_scope_spread",
        max(frob_production_pct) - min(frob_production_pct) < 12.0,
        f"range={max(frob_production_pct) - min(frob_production_pct):.3f} percentage points",
        "production-scope fixed-Frobenius spread stays below twelve percentage points",
        "The response scale is stable enough for a scoped finite-band mechanism claim.",
    )
    add(
        audit,
        "fixed_delta0_sign_sensitivity",
        min(delta_pct) < 0.0 < max(delta_pct),
        f"min={min(delta_pct):.3f}%, max={max(delta_pct):.3f}%",
        "fixed-Delta0 control includes both signs",
        "The normalization dependence remains visible in the stronger robustness matrix.",
    )
    add(
        audit,
        "numerical_error_bounds",
        max(floats(summary_rows, "max_ph_spectrum_error")) < 1.0e-8,
        f"max_ph={max(floats(summary_rows, 'max_ph_spectrum_error')):.3e}",
        "particle-hole spectrum error remains below 1e-8",
        "The robustness matrix is not dominated by BdG numerical symmetry failure.",
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
    print(f"PRB major-revision robustness checks passed: {pass_count}/{len(audit)}")
    failures = [row for row in audit if row.status != "pass"]
    if failures:
        for row in failures:
            print(f"FAIL: {row.check_id}: {row.measured_value}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
