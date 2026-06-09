#!/usr/bin/env python3
"""Audit mechanical readiness of the PRB manuscript package."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN_TEX = (
    ROOT
    / "Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex"
)
MAIN_PDF = MAIN_TEX.with_suffix(".pdf")
SUPP_TEX = (
    ROOT
    / "Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_Supplemental_Material_2026.tex"
)
SUPP_PDF = SUPP_TEX.with_suffix(".pdf")
COVER_LETTER = ROOT / "submission" / "Zhou_PRB_Cover_Letter_2026.md"

OUTPUT = ROOT / "data" / "processed" / "submission_package_audit.csv"

REQUIRED_AUTHOR_PHRASES = [
    r"\author{Jian Zhou}",
    r"\affiliation{JZ Institute of Science, Hong Kong, China}",
    r"\email{jack@jzis.org}",
]

PROHIBITED_AUTHOR_VARIANTS = [
    ("jack", "Jack"),
    ("jack_zhou", "Jack Zhou"),
    ("wall_e", "Wall-E"),
    ("wali_chinese", "瓦力"),
    ("j_zhou", "J. Zhou"),
    ("zhou_j", "Zhou, J."),
]

REQUIRED_DECLARATIONS = [
    r"\section*{Declarations}",
    r"\textbf{Funding}: Not applicable.",
    r"\textbf{Conflict of interest}: The author declares no conflict of interest.",
    r"\textbf{Data availability}: All data and code supporting this work are available",
    r"\textbf{Ethics approval}: Not applicable.",
]

COVER_LETTER_REQUIRED_PHRASES = [
    "Physical Review B",
    "Interband Pairing Signatures in the Superfluid Response of Magic-Angle Twisted Bilayer Graphene",
    "does not claim a final absolute stiffness prediction",
    "not under consideration elsewhere",
    "Sincerely,\nJian Zhou\nPrincipal Investigator\nJZ Institute of Science, Hong Kong, China\njack@jzis.org",
]

MAIN_REQUIRED_SECTIONS = [
    r"\section{Introduction}",
    r"\section{Model and Pairing Construction}",
    r"\section{Finite-Band Response}",
    r"\section{Pairing Gates and Response Maps}",
    r"\section{Self-Audit of Absolute Units}",
    r"\section{Discussion}",
    r"\section{Conclusions}",
]

SUPP_REQUIRED_SECTIONS = [
    r"\section{Scope of the Supplemental Material}",
    r"\section{BM Model and Numerical Parameters}",
    r"\section{Orbital-Projected Pairing Construction}",
    r"\section{Claim Scope and Excluded Interpretations}",
    r"\section{Current Limitations and Next Validation Gates}",
]

REQUIRED_MAIN_LABELS = [
    r"\label{fig:workflow}",
    r"\label{fig:heatmap_frob}",
    r"\label{fig:heatmap_delta0}",
    r"\label{tab:dense_eta}",
    r"\label{tab:nk9}",
    r"\label{tab:prb_audit}",
]

REQUIRED_SUPP_LABELS = [
    r"\label{tab:sm_reporting_layers}",
    r"\label{tab:sm_filling_crosswalk}",
    r"\label{tab:sm_filling_sufficiency}",
    r"\label{tab:sm_convergence_sufficiency}",
    r"\label{tab:sm_claim_scope}",
]


@dataclass(frozen=True)
class AuditRow:
    check_id: str
    scope: str
    status: str
    evidence: str
    requirement: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    return parser.parse_args()


def contains(text: str, phrase: str) -> bool:
    return " ".join(phrase.split()) in " ".join(text.split())


def read(path: Path) -> str:
    return path.read_text()


def add(
    rows: list[AuditRow],
    check_id: str,
    scope: str,
    ok: bool,
    evidence: str,
    requirement: str,
) -> None:
    rows.append(
        AuditRow(
            check_id=check_id,
            scope=scope,
            status="pass" if ok else "fail",
            evidence=evidence,
            requirement=requirement,
        )
    )


def audit_required_phrases(
    rows: list[AuditRow],
    text: str,
    scope: str,
    phrases: list[str],
    prefix: str,
) -> None:
    for index, phrase in enumerate(phrases, start=1):
        add(
            rows,
            f"{prefix}_{index:02d}",
            scope,
            contains(text, phrase),
            phrase,
            "Required manuscript/package phrase must be present.",
        )


def includegraphics_paths(text: str) -> list[str]:
    return re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text)


def audit_graphics(rows: list[AuditRow], text: str, scope: str) -> None:
    paths = includegraphics_paths(text)
    add(
        rows,
        f"{scope}_graphics_present",
        scope,
        bool(paths),
        f"{len(paths)} includegraphics command(s)",
        "At least one visual asset should be present in a PRB manuscript file.",
    )
    for index, raw_path in enumerate(paths, start=1):
        path = ROOT / raw_path
        add(
            rows,
            f"{scope}_graphic_exists_{index:02d}",
            scope,
            path.exists(),
            raw_path,
            "Every included graphic file must exist in the repository.",
        )


def main() -> int:
    args = parse_args()
    rows: list[AuditRow] = []

    main_exists = MAIN_TEX.exists()
    supp_exists = SUPP_TEX.exists()
    cover_exists = COVER_LETTER.exists()
    add(rows, "main_tex_exists", "main", main_exists, str(MAIN_TEX), "Main TeX file exists.")
    add(rows, "main_pdf_exists", "main", MAIN_PDF.exists(), str(MAIN_PDF), "Main PDF exists.")
    add(rows, "supp_tex_exists", "supplement", supp_exists, str(SUPP_TEX), "Supplement TeX exists.")
    add(rows, "supp_pdf_exists", "supplement", SUPP_PDF.exists(), str(SUPP_PDF), "Supplement PDF exists.")
    add(rows, "cover_letter_exists", "cover_letter", cover_exists, str(COVER_LETTER), "Cover letter draft exists.")

    main_text = read(MAIN_TEX) if main_exists else ""
    supp_text = read(SUPP_TEX) if supp_exists else ""
    cover_text = read(COVER_LETTER) if cover_exists else ""
    combined = f"{main_text}\n{supp_text}\n{cover_text}"

    add(
        rows,
        "main_filename_rule_tex",
        "main",
        MAIN_TEX.name
        == "Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex",
        MAIN_TEX.name,
        "Main paper TeX filename follows the Zhou_<Title>_2026.tex convention.",
    )
    add(
        rows,
        "main_filename_rule_pdf",
        "main",
        MAIN_PDF.name
        == "Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.pdf",
        MAIN_PDF.name,
        "Main paper PDF filename follows the Zhou_<Title>_2026.pdf convention.",
    )

    audit_required_phrases(
        rows,
        main_text,
        "main",
        [r"\documentclass[aps,prb,reprint,superscriptaddress,floatfix,nofootinbib]{revtex4-2}"],
        "main_revtex",
    )
    audit_required_phrases(rows, main_text, "main", [r"\begin{abstract}"], "main_abstract")
    audit_required_phrases(rows, main_text, "main", REQUIRED_AUTHOR_PHRASES, "main_author")
    audit_required_phrases(rows, supp_text, "supplement", REQUIRED_AUTHOR_PHRASES, "supp_author")
    audit_required_phrases(rows, main_text, "main", REQUIRED_DECLARATIONS, "main_declaration")
    audit_required_phrases(rows, supp_text, "supplement", REQUIRED_DECLARATIONS, "supp_declaration")
    audit_required_phrases(
        rows,
        cover_text,
        "cover_letter",
        COVER_LETTER_REQUIRED_PHRASES,
        "cover_letter",
    )
    audit_required_phrases(rows, main_text, "main", MAIN_REQUIRED_SECTIONS, "main_section")
    audit_required_phrases(rows, supp_text, "supplement", SUPP_REQUIRED_SECTIONS, "supp_section")
    audit_required_phrases(rows, main_text, "main", REQUIRED_MAIN_LABELS, "main_label")
    audit_required_phrases(rows, supp_text, "supplement", REQUIRED_SUPP_LABELS, "supp_label")
    audit_required_phrases(rows, main_text, "main", [r"\bibliography{references}"], "main_bibliography")
    audit_required_phrases(rows, supp_text, "supplement", [r"\bibliography{references}"], "supp_bibliography")

    for slug, variant in PROHIBITED_AUTHOR_VARIANTS:
        add(
            rows,
            f"forbid_author_variant_{slug}",
            "main+supplement+cover_letter",
            variant not in combined,
            variant,
            "Prohibited author-name variant must not appear in submission text files.",
        )

    audit_graphics(rows, main_text, "main")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["check_id", "scope", "status", "evidence", "requirement"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows([row.__dict__ for row in rows])

    pass_count = sum(row.status == "pass" for row in rows)
    print(f"Wrote {args.output}")
    print(f"Submission-package checks passed: {pass_count}/{len(rows)}")
    failures = [row for row in rows if row.status != "pass"]
    if failures:
        for row in failures:
            print(f"FAIL: {row.check_id}: {row.evidence}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
