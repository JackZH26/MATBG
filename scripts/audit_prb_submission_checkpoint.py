#!/usr/bin/env python3
"""Audit the local PRB submission checkpoint after package construction."""

from __future__ import annotations

import csv
import hashlib
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

MAIN_TITLE = "Interband Pairing Signatures in the Superfluid Response of Magic-Angle Twisted Bilayer Graphene"
MAIN_TEX = ROOT / "Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex"
MAIN_PDF = MAIN_TEX.with_suffix(".pdf")
SUPP_TEX = ROOT / "Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_Supplemental_Material_2026.tex"
SUPP_PDF = SUPP_TEX.with_suffix(".pdf")
COVER_LETTER = ROOT / "submission" / "Zhou_PRB_Cover_Letter_2026.md"
RESPONSE_LETTER = ROOT / "submission" / "Zhou_PRB_Response_To_Reviewers_2026.md"
README = ROOT / "README.md"
GITIGNORE = ROOT / ".gitignore"

MANIFEST = PROCESSED / "prb_submission_manifest.csv"
VALIDATION_SUMMARY = PROCESSED / "prb_validation_summary.csv"
PACKAGE_SUMMARY = PROCESSED / "prb_submission_package_build.csv"
GOAL_COMPLETION_AUDIT = PROCESSED / "prb_goal_completion_audit.csv"
OUTPUT = PROCESSED / "prb_submission_checkpoint_audit.csv"

EXPECTED_AUTHOR_BLOCKS = [
    r"\author{Jian Zhou}",
    r"\affiliation{JZ Institute of Science, Hong Kong, China}",
    r"\email{jack@jzis.org}",
]
EXPECTED_DECLARATIONS = [
    r"\section*{Declarations}",
    r"\textbf{Funding}: Not applicable.",
    r"\textbf{Conflict of interest}: The author declares no conflict of interest.",
    r"\textbf{Data availability}: All data and code supporting this work are available",
    r"\textbf{Ethics approval}: Not applicable.",
]
EXPECTED_COVER_SIGNATURE = (
    "Sincerely,\n"
    "Jian Zhou\n"
    "Principal Investigator\n"
    "JZ Institute of Science, Hong Kong, China\n"
    "jack@jzis.org"
)
FORBIDDEN_AUTHOR_VARIANTS = [
    ("jack", "Jack"),
    ("jack_zhou", "Jack Zhou"),
    ("wall_e", "Wall-E"),
    ("wali_chinese", "瓦力"),
    ("j_zhou", "J. Zhou"),
    ("zhou_j", "Zhou, J."),
]
REQUIRED_MANIFEST_IDS = {
    "main_tex",
    "main_pdf",
    "supplement_tex",
    "supplement_pdf",
    "cover_letter",
    "response_to_reviewers",
    "bibliography",
    "pairing_family_response_data",
    "pairing_family_response_summary",
    "pairing_family_response_audit",
    "major_revision_robustness_matrix",
    "major_revision_robustness_summary",
    "major_revision_robustness_audit",
    "valley_response_sensitivity_data",
    "valley_response_sensitivity_summary",
    "valley_response_sensitivity_audit",
    "major_revision_plan_note",
    "pairing_family_revision_note",
    "major_revision_robustness_note",
    "valley_response_sensitivity_note",
    "submission_package_build_summary",
    "prb_submission_checkpoint_audit",
    "prb_goal_completion_audit",
    "submission_checkpoint_audit_note",
    "goal_completion_audit_note",
}
REQUIRED_JOURNAL_UPLOADS = [
    MAIN_TEX,
    MAIN_PDF,
    SUPP_TEX,
    SUPP_PDF,
    COVER_LETTER,
    RESPONSE_LETTER,
    ROOT / "references.bib",
]
REQUIRED_PROVENANCE = [
    README,
    MANIFEST,
    VALIDATION_SUMMARY,
    PACKAGE_SUMMARY,
    OUTPUT,
    GOAL_COMPLETION_AUDIT,
]
JOURNAL_ROLES = {
    "journal_source",
    "journal_pdf",
    "journal_figure",
    "journal_submission_text",
}
PROVENANCE_ROLES = {
    "configuration",
    "source_data",
    "audit_output",
    "source_code",
    "validation_script",
    "provenance_note",
}
REQUIRED_VALIDATION_STEPS = {
    "python_compile_scripts",
    "claim_scope_audit",
    "observable_policy_audit",
    "filling_sufficiency_audit",
    "convergence_sufficiency_audit",
    "pairing_family_response_audit",
    "major_revision_robustness_audit",
    "valley_response_sensitivity_audit",
    "manuscript_table_verifier",
    "submission_package_audit",
    "submission_manifest_build",
    "main_latexmk",
    "supplement_latexmk",
    "main_latex_log_audit",
    "supplement_latex_log_audit",
}


@dataclass(frozen=True)
class AuditRow:
    check_id: str
    scope: str
    status: str
    evidence: str
    requirement: str


def normalize(text: str) -> str:
    return " ".join(text.split())


def contains(text: str, phrase: str) -> bool:
    return normalize(phrase) in normalize(text)


def read_text(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def author_sensitive_text(*texts: str) -> str:
    markers = (
        r"\author",
        r"\affiliation",
        r"\email",
        "author:",
        "sincerely,",
        "principal investigator",
        "jz institute",
    )
    lines = []
    for text in texts:
        for line in text.splitlines():
            lowered = line.lower()
            if any(marker in lowered for marker in markers):
                lines.append(line)
    return "\n".join(lines)


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


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def latex_title(text: str) -> str:
    match = re.search(r"\\title\{(.+?)\}", text, flags=re.S)
    return normalize(match.group(1)) if match else ""


def package_paths(summary_rows: list[dict[str, str]]) -> tuple[Path | None, Path | None, int | None, int | None, str]:
    if not summary_rows:
        return None, None, None, None, ""
    row = summary_rows[0]
    package_dir = ROOT / row.get("package_dir", "")
    zip_path = ROOT / row.get("zip_path", "")
    copied_files = int(row["copied_files"]) if row.get("copied_files", "").isdigit() else None
    manifest_entries = int(row["manifest_entries"]) if row.get("manifest_entries", "").isdigit() else None
    return package_dir, zip_path, copied_files, manifest_entries, row.get("status", "")


def package_contains(package_dir: Path | None, root_folder: str, source: Path) -> bool:
    if package_dir is None:
        return False
    return (package_dir / root_folder / source.relative_to(ROOT)).exists()


def artifact_slug(source: Path) -> str:
    return (
        str(source.relative_to(ROOT))
        .replace("/", "_")
        .replace(".", "_")
        .replace("-", "_")
    )


def zip_contains(zip_path: Path | None, package_dir: Path | None, root_folder: str, source: Path) -> bool:
    if zip_path is None or package_dir is None or not zip_path.exists():
        return False
    arcname = package_dir.name + "/" + root_folder + "/" + str(source.relative_to(ROOT))
    with zipfile.ZipFile(zip_path) as archive:
        return arcname in set(archive.namelist())


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def manifest_package_payloads(manifest_rows: list[dict[str, str]]) -> list[tuple[dict[str, str], str]]:
    payloads: list[tuple[dict[str, str], str]] = []
    for row in manifest_rows:
        role = row.get("role", "")
        if row.get("required") != "yes" or row.get("status") != "present":
            continue
        if role in JOURNAL_ROLES:
            payloads.append((row, "journal_upload"))
        elif role in PROVENANCE_ROLES:
            payloads.append((row, "provenance"))
    return payloads


def package_hash_mismatches(
    package_dir: Path | None,
    manifest_rows: list[dict[str, str]],
) -> list[str]:
    if package_dir is None:
        return ["missing package directory"]
    mismatches: list[str] = []
    for row, root_folder in manifest_package_payloads(manifest_rows):
        relative = row.get("path", "")
        expected_hash = row.get("sha256", "")
        packaged = package_dir / root_folder / relative
        if not packaged.exists():
            mismatches.append(f"{relative}: missing")
        elif expected_hash and sha256_file(packaged) != expected_hash:
            mismatches.append(f"{relative}: hash mismatch")
    return mismatches


def zip_hash_mismatches(
    zip_path: Path | None,
    package_dir: Path | None,
    manifest_rows: list[dict[str, str]],
) -> list[str]:
    if zip_path is None or package_dir is None or not zip_path.exists():
        return ["missing package zip"]
    mismatches: list[str] = []
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        for row, root_folder in manifest_package_payloads(manifest_rows):
            relative = row.get("path", "")
            expected_hash = row.get("sha256", "")
            arcname = package_dir.name + "/" + root_folder + "/" + relative
            if arcname not in names:
                mismatches.append(f"{relative}: missing")
            elif expected_hash and sha256_bytes(archive.read(arcname)) != expected_hash:
                mismatches.append(f"{relative}: hash mismatch")
    return mismatches


def main() -> int:
    rows: list[AuditRow] = []

    main_text = read_text(MAIN_TEX)
    supp_text = read_text(SUPP_TEX)
    cover_text = read_text(COVER_LETTER)
    response_text = read_text(RESPONSE_LETTER)
    readme_text = read_text(README)
    author_text = author_sensitive_text(main_text, supp_text, cover_text, response_text)

    manifest_rows = load_csv(MANIFEST)
    validation_rows = load_csv(VALIDATION_SUMMARY)
    package_summary_rows = load_csv(PACKAGE_SUMMARY)
    package_dir, zip_path, copied_files, manifest_entries, package_status = package_paths(package_summary_rows)

    add(rows, "title_main_tex", "title", latex_title(main_text) == MAIN_TITLE, latex_title(main_text), "Main TeX title matches the PRB checkpoint title.")
    add(rows, "title_supplement_tex", "title", MAIN_TITLE in supp_text, MAIN_TITLE, "Supplement title references the same manuscript title.")
    add(rows, "title_cover_letter", "title", contains(cover_text, MAIN_TITLE), MAIN_TITLE, "Cover letter uses the same manuscript title.")
    add(rows, "title_response_letter", "title", contains(response_text, MAIN_TITLE), MAIN_TITLE, "Response-to-reviewers letter uses the same manuscript title.")
    add(rows, "title_readme_files", "title", MAIN_TEX.name in readme_text and SUPP_TEX.name in readme_text, "main and supplement filenames", "README lists the active manuscript and supplement files.")

    for phrase in EXPECTED_AUTHOR_BLOCKS:
        add(rows, f"main_author_{len([r for r in rows if r.check_id.startswith('main_author_')]) + 1:02d}", "authorship", contains(main_text, phrase), phrase, "Main TeX author block matches the required Jian Zhou metadata.")
        add(rows, f"supp_author_{len([r for r in rows if r.check_id.startswith('supp_author_')]) + 1:02d}", "authorship", contains(supp_text, phrase), phrase, "Supplement author block matches the required Jian Zhou metadata.")
    add(rows, "cover_signature", "authorship", EXPECTED_COVER_SIGNATURE in cover_text, "Jian Zhou signature", "Cover letter uses the required signature.")
    add(rows, "response_signature", "authorship", EXPECTED_COVER_SIGNATURE in response_text, "Jian Zhou signature", "Response-to-reviewers letter uses the required signature.")
    for slug, variant in FORBIDDEN_AUTHOR_VARIANTS:
        add(rows, f"forbid_author_variant_{slug}", "authorship", variant not in author_text, variant, "Forbidden author-name variants are absent from author fields and signature metadata.")

    for phrase in EXPECTED_DECLARATIONS:
        add(rows, f"main_declaration_{len([r for r in rows if r.check_id.startswith('main_declaration_')]) + 1:02d}", "declarations", contains(main_text, phrase), phrase, "Main TeX contains the required declarations.")
        add(rows, f"supp_declaration_{len([r for r in rows if r.check_id.startswith('supp_declaration_')]) + 1:02d}", "declarations", contains(supp_text, phrase), phrase, "Supplement contains the required declarations.")

    add(rows, "readme_scope_status", "readme", contains(readme_text, "local PRB major-revision response package"), "major-revision package scope", "README states the current local PRB major-revision package status.")
    add(rows, "readme_validation_command", "readme", "python3 scripts/run_prb_validation.py" in readme_text, "run_prb_validation.py", "README documents the standard validation command.")
    add(rows, "readme_package_command", "readme", "python3 scripts/build_prb_submission_package.py" in readme_text, "build_prb_submission_package.py", "README documents the local package command.")
    add(rows, "readme_checkpoint_audit_command", "readme", "python3 scripts/audit_prb_submission_checkpoint.py" in readme_text, "audit_prb_submission_checkpoint.py", "README documents the final checkpoint audit command.")
    add(rows, "readme_goal_completion_audit", "readme", "prb_goal_completion_audit.csv" in readme_text, "prb_goal_completion_audit.csv", "README documents the goal-level completion audit.")
    add(rows, "readme_major_revision_scope", "readme", "major-revision response package" in readme_text, "major-revision response package", "README documents the current major-revision checkpoint scope.")

    add(rows, "validation_summary_exists", "validation", bool(validation_rows), str(VALIDATION_SUMMARY), "Validation summary CSV exists.")
    add(rows, "validation_summary_all_pass", "validation", bool(validation_rows) and all(row.get("status") == "pass" for row in validation_rows), f"{sum(row.get('status') == 'pass' for row in validation_rows)}/{len(validation_rows)}", "All recorded validation rows pass.")
    validation_steps = {row.get("step", "") for row in validation_rows}
    missing_validation_steps = sorted(REQUIRED_VALIDATION_STEPS - validation_steps)
    add(rows, "validation_required_steps", "validation", not missing_validation_steps, ",".join(missing_validation_steps) or "all present", "Validation summary includes all required major-revision validation steps.")

    manifest_ids = {row.get("artifact_id", "") for row in manifest_rows}
    missing_manifest_ids = sorted(REQUIRED_MANIFEST_IDS - manifest_ids)
    add(rows, "manifest_exists", "manifest", bool(manifest_rows), str(MANIFEST), "Submission manifest exists.")
    add(rows, "manifest_required_ids", "manifest", not missing_manifest_ids, ",".join(missing_manifest_ids) or "all present", "Manifest contains the final checkpoint-required artifact IDs.")
    add(rows, "manifest_all_required_present", "manifest", bool(manifest_rows) and all(row.get("status") == "present" for row in manifest_rows if row.get("required") == "yes"), f"{sum(row.get('status') == 'present' for row in manifest_rows if row.get('required') == 'yes')}/{sum(row.get('required') == 'yes' for row in manifest_rows)}", "All required manifest rows are present.")

    add(rows, "package_summary_exists", "package", bool(package_summary_rows), str(PACKAGE_SUMMARY), "Package build summary exists.")
    add(rows, "package_summary_pass", "package", package_status == "pass", package_status, "Package build summary status is pass.")
    add(rows, "package_dir_exists", "package", package_dir is not None and package_dir.exists(), str(package_dir), "Ignored local package directory exists.")
    add(rows, "package_zip_exists", "package", zip_path is not None and zip_path.exists(), str(zip_path), "Ignored local package zip exists.")
    add(rows, "package_count_matches_manifest", "package", copied_files == (manifest_entries + 3 if manifest_entries is not None else None), f"copied={copied_files}, manifest={manifest_entries}", "Package copies all manifest files plus manifest, validation summary, and README extras.")
    add(rows, "manifest_count_matches_summary", "package", manifest_entries == len(manifest_rows), f"summary={manifest_entries}, manifest_rows={len(manifest_rows)}", "Package summary manifest-entry count matches the current manifest.")
    add(rows, "package_build_ignored", "package", "submission/build/" in read_text(GITIGNORE), "submission/build/", "Ignored package outputs are excluded from git.")
    add(rows, "package_readme_exists", "package", package_dir is not None and (package_dir / "README_PACKAGE.md").exists(), "README_PACKAGE.md", "Package includes a package README.")
    package_mismatches = package_hash_mismatches(package_dir, manifest_rows)
    zip_mismatches = zip_hash_mismatches(zip_path, package_dir, manifest_rows)
    add(rows, "package_manifest_hashes_match", "package", not package_mismatches, f"{len(package_mismatches)} mismatch(es)", "All manifest-tracked files in the package directory match their recorded SHA-256 hashes.")
    add(rows, "zip_manifest_hashes_match", "package", not zip_mismatches, f"{len(zip_mismatches)} mismatch(es)", "All manifest-tracked files in the package zip match their recorded SHA-256 hashes.")

    for source in REQUIRED_JOURNAL_UPLOADS:
        slug = artifact_slug(source)
        add(rows, f"package_journal_{slug}", "package", package_contains(package_dir, "journal_upload", source), str(source.relative_to(ROOT)), "Journal upload package contains the required manuscript-facing file.")
        add(rows, f"zip_journal_{slug}", "package", zip_contains(zip_path, package_dir, "journal_upload", source), str(source.relative_to(ROOT)), "Package zip contains the required manuscript-facing file.")
    for source in REQUIRED_PROVENANCE:
        slug = artifact_slug(source)
        add(rows, f"package_provenance_{slug}", "package", package_contains(package_dir, "provenance", source), str(source.relative_to(ROOT)), "Package provenance directory contains the required file.")
        add(rows, f"zip_provenance_{slug}", "package", zip_contains(zip_path, package_dir, "provenance", source), str(source.relative_to(ROOT)), "Package zip contains the required provenance file.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["check_id", "scope", "status", "evidence", "requirement"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows([row.__dict__ for row in rows])

    pass_count = sum(row.status == "pass" for row in rows)
    print(f"Wrote {OUTPUT}")
    print(f"PRB submission checkpoint checks passed: {pass_count}/{len(rows)}")
    failures = [row for row in rows if row.status != "pass"]
    if failures:
        for row in failures:
            print(f"FAIL: {row.check_id}: {row.evidence}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
