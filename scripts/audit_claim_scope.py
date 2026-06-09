#!/usr/bin/env python3
"""Audit manuscript claim scope against the current PRB mechanism framing."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN_TEX = (
    ROOT
    / "Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex"
)
SUPP_TEX = (
    ROOT
    / "Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_Supplemental_Material_2026.tex"
)


@dataclass(frozen=True)
class RequiredPhrase:
    check_id: str
    scope: str
    phrase: str
    reason: str


@dataclass(frozen=True)
class ForbiddenPhrase:
    check_id: str
    phrase: str
    reason: str


REQUIRED_PHRASES = [
    RequiredPhrase(
        "main_normalization_conditioned",
        "main",
        "normalization-conditioned mechanism signature",
        "Central result must remain conditional on the normalization protocol.",
    ),
    RequiredPhrase(
        "main_not_absolute_prediction",
        "main",
        "not an absolute stiffness prediction",
        "Main text must not promote raw response values to physical stiffness.",
    ),
    RequiredPhrase(
        "main_not_dome_map",
        "main",
        "not as a quantitative map onto an experimental superconducting dome",
        "Filling crosswalk is not a device-level carrier-density calibration.",
    ),
    RequiredPhrase(
        "main_delta0_control",
        "main",
        "fixed-$\\Delta_0$ control remains weak",
        "The weaker fixed-Delta0 control limits unconditional enhancement claims.",
    ),
    RequiredPhrase(
        "main_nk15_spotcheck",
        "main",
        "targeted $nk=15$ spot check",
        "Main text should reflect the latest high-grid representative check.",
    ),
    RequiredPhrase(
        "main_convergence_sufficiency_scope",
        "main",
        "selected-grid normalized mechanism claim",
        "Main text should state the finite-grid claim scope supported by the audit.",
    ),
    RequiredPhrase(
        "supp_no_final_experimental_stiffness",
        "supplement",
        "does not promote the raw response units to final experimental stiffness values",
        "Supplement must declare the absolute-unit boundary.",
    ),
    RequiredPhrase(
        "supp_device_calibration_boundary",
        "supplement",
        "not as a device-specific carrier-density calibration",
        "Central-flat-band crosswalk must not be overinterpreted.",
    ),
    RequiredPhrase(
        "supp_not_continuum_extrapolation",
        "supplement",
        "rather than a final continuum extrapolation",
        "Finite-grid trend audit must not be sold as a continuum limit.",
    ),
    RequiredPhrase(
        "supp_not_dense_replacement",
        "supplement",
        "not a full dense-grid replacement",
        "The nk15 result is a targeted spot check only.",
    ),
    RequiredPhrase(
        "supp_convergence_sufficiency_table",
        "supplement",
        "\\label{tab:sm_convergence_sufficiency}",
        "Supplement should expose the convergence-sufficiency self-audit.",
    ),
    RequiredPhrase(
        "supp_claim_scope_table",
        "supplement",
        "\\label{tab:sm_claim_scope}",
        "Supplement should expose the allowed and excluded claim scope.",
    ),
]

FORBIDDEN_PHRASES = [
    ForbiddenPhrase(
        "forbid_universal_enhancement",
        "universally enhances physical stiffness",
        "The fixed-Delta0 control contradicts a universal enhancement claim.",
    ),
    ForbiddenPhrase(
        "forbid_quant_agreement",
        "quantitative agreement with experimental stiffness",
        "Direct experimental stiffness comparison is outside the current scope.",
    ),
    ForbiddenPhrase(
        "forbid_final_carrier_density",
        "device-level carrier-density calibration is complete",
        "The current filling work is a central-flat-band crosswalk only.",
    ),
    ForbiddenPhrase(
        "forbid_final_continuum_limit",
        "final continuum-limit estimate",
        "The present convergence layer is finite-grid and selected-point only.",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "claim_scope_audit.csv",
    )
    return parser.parse_args()


def text_for_scope(scope: str, main_text: str, supp_text: str) -> str:
    if scope == "main":
        return main_text
    if scope == "supplement":
        return supp_text
    raise ValueError(f"Unknown scope: {scope}")


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def contains_phrase(text: str, phrase: str) -> bool:
    return normalize_whitespace(phrase) in normalize_whitespace(text)


def main() -> int:
    args = parse_args()
    main_text = MAIN_TEX.read_text()
    supp_text = SUPP_TEX.read_text()
    combined = f"{main_text}\n{supp_text}"

    rows: list[dict[str, str]] = []
    failures: list[str] = []

    for item in REQUIRED_PHRASES:
        found = contains_phrase(
            text_for_scope(item.scope, main_text, supp_text),
            item.phrase,
        )
        rows.append(
            {
                "check_id": item.check_id,
                "kind": "required_phrase",
                "scope": item.scope,
                "status": "pass" if found else "fail",
                "phrase": item.phrase,
                "reason": item.reason,
            }
        )
        if not found:
            failures.append(f"Missing required phrase: {item.check_id}")

    combined_lower = normalize_whitespace(combined).lower()
    for item in FORBIDDEN_PHRASES:
        found = normalize_whitespace(item.phrase).lower() in combined_lower
        rows.append(
            {
                "check_id": item.check_id,
                "kind": "forbidden_phrase",
                "scope": "main+supplement",
                "status": "fail" if found else "pass",
                "phrase": item.phrase,
                "reason": item.reason,
            }
        )
        if found:
            failures.append(f"Forbidden phrase present: {item.check_id}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["check_id", "kind", "scope", "status", "phrase", "reason"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    pass_count = sum(row["status"] == "pass" for row in rows)
    print(f"Wrote {args.output}")
    print(f"Claim-scope checks passed: {pass_count}/{len(rows)}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
