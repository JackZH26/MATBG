#!/usr/bin/env python3
"""Build a local PRB submission checkpoint package from the manifest."""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "processed" / "prb_submission_manifest.csv"
SUMMARY = ROOT / "data" / "processed" / "prb_submission_package_build.csv"
BUILD_ROOT = ROOT / "submission" / "build"
DEFAULT_PACKAGE_NAME = "MATBG_PRB_submission_checkpoint_2026-06-10"

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


@dataclass(frozen=True)
class ManifestRow:
    artifact_id: str
    role: str
    path: Path
    required: bool
    status: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-name", default=DEFAULT_PACKAGE_NAME)
    parser.add_argument("--output-root", type=Path, default=BUILD_ROOT)
    parser.add_argument("--summary", type=Path, default=SUMMARY)
    parser.add_argument(
        "--skip-manifest-refresh",
        action="store_true",
        help="Do not run build_prb_submission_manifest.py before packaging.",
    )
    return parser.parse_args()


def refresh_manifest() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/build_prb_submission_manifest.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stdout)


def load_manifest(path: Path) -> list[ManifestRow]:
    with path.open(newline="") as handle:
        rows = []
        for row in csv.DictReader(handle):
            rows.append(
                ManifestRow(
                    artifact_id=row["artifact_id"],
                    role=row["role"],
                    path=ROOT / row["path"],
                    required=row["required"] == "yes",
                    status=row["status"],
                )
            )
    return rows


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def package_readme(package_name: str, copied_count: int) -> str:
    return f"""# MATBG PRB Submission Checkpoint

Package: `{package_name}`

This directory is a local checkpoint package for the PRB-targeted manuscript
"Interband Pairing Signatures in the Superfluid Response of Magic-Angle
Twisted Bilayer Graphene".

## Directories

- `journal_upload/`: manuscript source/PDF, Supplemental Material source/PDF,
  cover letter draft, bibliography, and included figure files.
- `provenance/`: source-data CSV files, audit outputs, validation scripts, and
  provenance notes used to support the current checkpoint.

## Scope

This package reflects the current major-revision normalized-response
mechanism-paper scope.  It includes the point-by-point response draft, the
pairing-family scan, the grid/truncation/shell robustness matrix, and the
valley-partner response-sensitivity audit. It is not an APS Editorial Manager
upload until the author approves the final journal submission.

Files copied into checkpoint: {copied_count}
"""


def zip_directory(source_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source_dir.parent))


def write_summary(
    path: Path,
    package_dir: Path,
    zip_path: Path,
    copied_count: int,
    manifest_count: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "package_dir",
                "zip_path",
                "copied_files",
                "manifest_entries",
                "status",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerow(
            {
                "package_dir": str(package_dir.relative_to(ROOT)),
                "zip_path": str(zip_path.relative_to(ROOT)),
                "copied_files": copied_count,
                "manifest_entries": manifest_count,
                "status": "pass",
            }
        )


def main() -> int:
    args = parse_args()
    if not args.skip_manifest_refresh:
        refresh_manifest()

    rows = load_manifest(MANIFEST)
    missing = [row for row in rows if row.required and (row.status != "present" or not row.path.exists())]
    if missing:
        for row in missing:
            print(f"FAIL: missing {row.artifact_id} at {row.path.relative_to(ROOT)}")
        return 1

    package_dir = args.output_root / args.package_name
    zip_path = args.output_root / f"{args.package_name}.zip"
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True, exist_ok=True)

    copied_count = 0
    for row in rows:
        if row.role in JOURNAL_ROLES:
            destination = package_dir / "journal_upload" / row.path.relative_to(ROOT)
        elif row.role in PROVENANCE_ROLES:
            destination = package_dir / "provenance" / row.path.relative_to(ROOT)
        else:
            continue
        copy_file(row.path, destination)
        copied_count += 1

    extra_files = [
        ROOT / "data" / "processed" / "prb_submission_manifest.csv",
        ROOT / "data" / "processed" / "prb_validation_summary.csv",
        ROOT / "README.md",
    ]
    for source in extra_files:
        copy_file(source, package_dir / "provenance" / source.relative_to(ROOT))
        copied_count += 1

    (package_dir / "README_PACKAGE.md").write_text(
        package_readme(args.package_name, copied_count)
    )
    zip_directory(package_dir, zip_path)
    write_summary(args.summary, package_dir, zip_path, copied_count, len(rows))

    print(f"Wrote {package_dir}")
    print(f"Wrote {zip_path}")
    print(f"Wrote {args.summary}")
    print(f"Copied files: {copied_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
