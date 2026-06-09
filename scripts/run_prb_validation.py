#!/usr/bin/env python3
"""Run the lightweight PRB manuscript validation chain."""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = PROCESSED / "prb_validation_summary.csv"

MAIN_TEX = (
    ROOT
    / "Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex"
)
SUPP_TEX = (
    ROOT
    / "Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_Supplemental_Material_2026.tex"
)


@dataclass(frozen=True)
class ValidationRow:
    step: str
    command: str
    status: str
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--skip-latex",
        action="store_true",
        help="Skip latexmk compilation and log checks.",
    )
    return parser.parse_args()


def command_text(command: list[str]) -> str:
    return " ".join(command)


def excerpt(text: str, limit: int = 500) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def run_command(step: str, command: list[str]) -> ValidationRow:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    status = "pass" if result.returncode == 0 else "fail"
    detail = excerpt(result.stdout)
    return ValidationRow(
        step=step,
        command=command_text(command),
        status=status,
        detail=detail,
    )


def log_blockers(path: Path) -> list[str]:
    text = path.read_text(errors="replace")
    blockers = []
    patterns = [
        "LaTeX Error",
        "Undefined control sequence",
        "LaTeX Warning: There were undefined references",
        "undefined references",
        "Citation",
        "Package natbib Warning",
        "Overfull \\hbox",
        "Overfull \\vbox",
    ]
    for line in text.splitlines():
        if any(pattern in line for pattern in patterns):
            blockers.append(line.strip())
    return blockers


def audit_log(step: str, path: Path) -> ValidationRow:
    if not path.exists():
        return ValidationRow(
            step=step,
            command=f"read {path.name}",
            status="fail",
            detail="log file does not exist",
        )
    blockers = log_blockers(path)
    return ValidationRow(
        step=step,
        command=f"scan {path.name}",
        status="pass" if not blockers else "fail",
        detail="no blocking LaTeX log warnings"
        if not blockers
        else excerpt("; ".join(blockers), limit=900),
    )


def validation_commands() -> list[tuple[str, list[str]]]:
    scripts = sorted(str(path.relative_to(ROOT)) for path in (ROOT / "scripts").glob("*.py"))
    return [
        ("python_compile_scripts", [sys.executable, "-m", "py_compile", *scripts]),
        ("claim_scope_audit", [sys.executable, "scripts/audit_claim_scope.py"]),
        ("observable_policy_audit", [sys.executable, "scripts/audit_observable_policy.py"]),
        ("filling_sufficiency_audit", [sys.executable, "scripts/audit_filling_sufficiency.py"]),
        ("convergence_sufficiency_audit", [sys.executable, "scripts/audit_convergence_sufficiency.py"]),
        ("manuscript_table_verifier", [sys.executable, "scripts/verify_manuscript_tables.py"]),
        ("submission_package_audit", [sys.executable, "scripts/audit_submission_package.py"]),
        ("submission_manifest_build", [sys.executable, "scripts/build_prb_submission_manifest.py"]),
    ]


def latex_commands() -> list[tuple[str, list[str]]]:
    return [
        (
            "main_latexmk",
            [
                "latexmk",
                "-pdf",
                "-interaction=nonstopmode",
                "-halt-on-error",
                MAIN_TEX.name,
            ],
        ),
        (
            "supplement_latexmk",
            [
                "latexmk",
                "-pdf",
                "-interaction=nonstopmode",
                "-halt-on-error",
                SUPP_TEX.name,
            ],
        ),
    ]


def write_rows(path: Path, rows: list[ValidationRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["step", "command", "status", "detail"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows([row.__dict__ for row in rows])


def main() -> int:
    args = parse_args()
    rows: list[ValidationRow] = []

    for step, command in validation_commands():
        row = run_command(step, command)
        rows.append(row)
        print(f"{step}: {row.status}")
        if row.status != "pass":
            write_rows(args.output, rows)
            print(f"Wrote {args.output}")
            return 1

    if not args.skip_latex:
        for step, command in latex_commands():
            row = run_command(step, command)
            rows.append(row)
            print(f"{step}: {row.status}")
            if row.status != "pass":
                write_rows(args.output, rows)
                print(f"Wrote {args.output}")
                return 1
        rows.append(audit_log("main_latex_log_audit", MAIN_TEX.with_suffix(".log")))
        rows.append(audit_log("supplement_latex_log_audit", SUPP_TEX.with_suffix(".log")))
        print(f"main_latex_log_audit: {rows[-2].status}")
        print(f"supplement_latex_log_audit: {rows[-1].status}")

    write_rows(args.output, rows)
    pass_count = sum(row.status == "pass" for row in rows)
    print(f"Wrote {args.output}")
    print(f"PRB validation checks passed: {pass_count}/{len(rows)}")
    return 0 if pass_count == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
