#!/usr/bin/env python3
"""Build a deterministic manifest for the PRB manuscript package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = PROCESSED / "prb_submission_manifest.csv"

MAIN_TEX = (
    ROOT
    / "Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex"
)
SUPP_TEX = (
    ROOT
    / "Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_Supplemental_Material_2026.tex"
)


@dataclass(frozen=True)
class ManifestItem:
    artifact_id: str
    role: str
    path: Path
    required: bool
    notes: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    return parser.parse_args()


def includegraphics_paths(tex_path: Path) -> list[Path]:
    if not tex_path.exists():
        return []
    text = tex_path.read_text()
    raw_paths = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text)
    return [ROOT / raw_path for raw_path in raw_paths]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def base_items() -> list[ManifestItem]:
    return [
        ManifestItem("main_tex", "journal_source", MAIN_TEX, True, "Current PRB-targeted main manuscript source."),
        ManifestItem("main_pdf", "journal_pdf", MAIN_TEX.with_suffix(".pdf"), True, "Compiled main manuscript PDF."),
        ManifestItem("supplement_tex", "journal_source", SUPP_TEX, True, "Supplemental Material source."),
        ManifestItem("supplement_pdf", "journal_pdf", SUPP_TEX.with_suffix(".pdf"), True, "Compiled Supplemental Material PDF."),
        ManifestItem("bibliography", "journal_source", ROOT / "references.bib", True, "Shared BibTeX database."),
        ManifestItem("dense_response_data", "source_data", PROCESSED / "mu_eta_response_scan_nk7_nkeep6.csv", True, "Dense mu-eta response map source data."),
        ManifestItem("dense_response_summary", "source_data", PROCESSED / "mu_eta_response_scan_nk7_nkeep6_eta1_summary.csv", True, "Main dense eta=1 response table source."),
        ManifestItem("nk9_summary", "source_data", PROCESSED / "mu_response_scan_nk9_nkeep6_keypoints_summary.csv", True, "Main nk=9 validation table source."),
        ManifestItem("nk11_summary", "source_data", PROCESSED / "mu_response_scan_nk11_nkeep6_keypoints_summary.csv", True, "Supplemental convergence table source."),
        ManifestItem("nk13_summary", "source_data", PROCESSED / "mu_response_scan_nk13_nkeep6_keypoints_summary.csv", True, "Supplemental convergence table source."),
        ManifestItem("nk15_summary", "source_data", PROCESSED / "mu_response_scan_nk15_nkeep6_spotcheck_summary.csv", True, "Supplemental nk=15 spot-check table source."),
        ManifestItem("filling_crosswalk", "source_data", PROCESSED / "filling_crosswalk_nk7_nshell3.csv", True, "Central-flat-band filling crosswalk."),
        ManifestItem("filling_sufficiency", "audit_output", PROCESSED / "filling_sufficiency_audit.csv", True, "Filling-sufficiency self-audit."),
        ManifestItem("convergence_sufficiency", "audit_output", PROCESSED / "convergence_sufficiency_audit.csv", True, "Convergence-sufficiency self-audit."),
        ManifestItem("claim_scope", "audit_output", PROCESSED / "claim_scope_audit.csv", True, "Text-level claim-scope guardrail."),
        ManifestItem("observable_policy", "audit_output", PROCESSED / "observable_policy_audit.csv", True, "Observable-policy guardrail."),
        ManifestItem("submission_package_audit", "audit_output", PROCESSED / "submission_package_audit.csv", True, "Mechanical submission-package audit."),
        ManifestItem("table_verifier", "validation_script", ROOT / "scripts" / "verify_manuscript_tables.py", True, "Table-value verification script."),
        ManifestItem("validation_chain", "validation_script", ROOT / "scripts" / "run_prb_validation.py", True, "One-command validation chain."),
        ManifestItem("figure_table_provenance", "provenance_note", ROOT / "notes" / "figure_table_provenance_2026-06-09.md", True, "Figure/table provenance manifest."),
        ManifestItem("readiness_audit", "provenance_note", ROOT / "notes" / "prb_readiness_audit_2026-06-09.md", True, "Current PRB readiness audit."),
        ManifestItem("validation_chain_note", "provenance_note", ROOT / "notes" / "prb_validation_chain_2026-06-09.md", True, "Validation-chain description."),
        ManifestItem("submission_manifest_note", "provenance_note", ROOT / "notes" / "prb_submission_manifest_2026-06-09.md", True, "Submission-manifest description."),
        ManifestItem("recent_literature_note", "provenance_note", ROOT / "notes" / "recent_literature_update_2026-06-09.md", True, "Latest recorded literature sweep."),
    ]


def figure_items() -> list[ManifestItem]:
    items: list[ManifestItem] = []
    seen: set[Path] = set()
    for scope, tex_path in (("main", MAIN_TEX), ("supplement", SUPP_TEX)):
        for index, path in enumerate(includegraphics_paths(tex_path), start=1):
            if path in seen:
                continue
            seen.add(path)
            items.append(
                ManifestItem(
                    artifact_id=f"{scope}_figure_{index:02d}",
                    role="journal_figure",
                    path=path,
                    required=True,
                    notes=f"Graphic included by the {scope} TeX file.",
                )
            )
    return items


def row_for(item: ManifestItem) -> dict[str, str]:
    exists = item.path.exists()
    return {
        "artifact_id": item.artifact_id,
        "role": item.role,
        "path": rel(item.path),
        "required": "yes" if item.required else "no",
        "status": "present" if exists else "missing",
        "size_bytes": str(item.path.stat().st_size) if exists else "",
        "sha256": sha256(item.path) if exists else "",
        "notes": item.notes,
    }


def main() -> int:
    args = parse_args()
    items = base_items() + figure_items()
    rows = [row_for(item) for item in items]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "artifact_id",
                "role",
                "path",
                "required",
                "status",
                "size_bytes",
                "sha256",
                "notes",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    missing = [row for row in rows if row["required"] == "yes" and row["status"] != "present"]
    print(f"Wrote {args.output}")
    print(f"PRB submission manifest entries present: {len(rows) - len(missing)}/{len(rows)}")
    if missing:
        for row in missing:
            print(f"FAIL: missing {row['artifact_id']} at {row['path']}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
