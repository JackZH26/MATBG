#!/usr/bin/env python3
"""Audit the manuscript's normalized-response observable policy."""

from __future__ import annotations

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
STRATEGY = ROOT / "notes" / "prb_manuscript_strategy_2026-06-09.md"
READINESS = ROOT / "notes" / "prb_readiness_audit_2026-06-10.md"
UNITS = ROOT / "notes" / "normalization_and_units_strategy.md"
OUTPUT = ROOT / "data" / "processed" / "observable_policy_audit.csv"


@dataclass(frozen=True)
class PhraseCheck:
    check_id: str
    file_key: str
    phrase: str
    reason: str


REQUIRED = [
    PhraseCheck(
        "main_claim_bearing_ratios",
        "main",
        "Normalized response ratios are the claim-bearing quantities",
        "Main text must state which response observable carries the claim.",
    ),
    PhraseCheck(
        "main_no_claim_bearing_absolute",
        "main",
        "makes no claim-bearing absolute stiffness prediction",
        "Main text must exclude absolute stiffness prediction claims.",
    ),
    PhraseCheck(
        "main_declared_diagnostic_convention",
        "main",
        "declared finite-band diagnostic convention",
        "Main text must bind the claim to the audited finite-band convention.",
    ),
    PhraseCheck(
        "supp_final_policy",
        "supplement",
        "final observable policy for the current mechanism-paper scope",
        "Supplement must expose the current mechanism-paper reporting policy.",
    ),
    PhraseCheck(
        "supp_claim_bearing_table",
        "supplement",
        "claim-bearing mechanism observable",
        "Supplemental reporting table must identify the claim-bearing row.",
    ),
    PhraseCheck(
        "supp_valley_boundary",
        "supplement",
        "valley-basis-independent stiffness claim",
        "Supplement must expose the valley-partner boundary after the sensitivity audit.",
    ),
    PhraseCheck(
        "strategy_policy",
        "strategy",
        "Final Observable Policy",
        "Strategy note must record the scope decision.",
    ),
    PhraseCheck(
        "readiness_scope",
        "readiness",
        "final observable policy for the current mechanism-paper scope",
        "Readiness audit must not treat absolute values as current-scope claims.",
    ),
    PhraseCheck(
        "units_claim_layer",
        "units",
        "final claim-bearing observable layer",
        "Units note must identify normalized ratios as the active claim layer.",
    ),
]

FORBIDDEN = [
    PhraseCheck(
        "old_absolute_blocker",
        "combined",
        "absolute response convention is not yet final for experimental stiffness comparison",
        "Old blocker wording should not remain after adopting normalized-only scope.",
    ),
    PhraseCheck(
        "old_must_choose_absolute",
        "combined",
        "final paper must still choose one absolute convention",
        "Current mechanism-paper scope should not require an absolute table.",
    ),
    PhraseCheck(
        "old_prevent_submission",
        "combined",
        "prevent the current draft from being treated as a final PRB submission",
        "Limitations should define scope rather than overstate an absolute blocker.",
    ),
]


def normalize(text: str) -> str:
    return " ".join(text.split())


def load_texts() -> dict[str, str]:
    texts = {
        "main": MAIN_TEX.read_text(),
        "supplement": SUPP_TEX.read_text(),
        "strategy": STRATEGY.read_text(),
        "readiness": READINESS.read_text(),
        "units": UNITS.read_text(),
    }
    texts["combined"] = "\n".join(texts.values())
    return texts


def contains(text: str, phrase: str) -> bool:
    return normalize(phrase).lower() in normalize(text).lower()


def main() -> int:
    texts = load_texts()
    rows: list[dict[str, str]] = []
    failures: list[str] = []

    for item in REQUIRED:
        found = contains(texts[item.file_key], item.phrase)
        status = "pass" if found else "fail"
        rows.append(
            {
                "check_id": item.check_id,
                "kind": "required_phrase",
                "file_key": item.file_key,
                "status": status,
                "phrase": item.phrase,
                "reason": item.reason,
            }
        )
        if not found:
            failures.append(f"Missing required phrase: {item.check_id}")

    for item in FORBIDDEN:
        found = contains(texts[item.file_key], item.phrase)
        status = "fail" if found else "pass"
        rows.append(
            {
                "check_id": item.check_id,
                "kind": "forbidden_phrase",
                "file_key": item.file_key,
                "status": status,
                "phrase": item.phrase,
                "reason": item.reason,
            }
        )
        if found:
            failures.append(f"Forbidden phrase present: {item.check_id}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["check_id", "kind", "file_key", "status", "phrase", "reason"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    pass_count = sum(row["status"] == "pass" for row in rows)
    print(f"Wrote {OUTPUT}")
    print(f"Observable-policy checks passed: {pass_count}/{len(rows)}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
