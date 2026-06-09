# PRB Submission Package Build

Date: 2026-06-09

## Purpose

This note records the local build step for a PRB submission checkpoint package.
The build step uses `data/processed/prb_submission_manifest.csv` as the source
inventory and copies the current journal-facing files and provenance files into
an ignored local directory under `submission/build/`.

## Command

```bash
python3 scripts/build_prb_submission_package.py
```

Outputs:

```text
submission/build/MATBG_PRB_submission_checkpoint_2026-06-09/
submission/build/MATBG_PRB_submission_checkpoint_2026-06-09.zip
data/processed/prb_submission_package_build.csv
```

The `submission/build/` directory is intentionally ignored by git because it
duplicates tracked manuscript PDFs, figures, data tables, scripts, and notes.
The tracked build summary records the package directory, zip path, number of
copied files, and pass/fail status.

## Current Scope

The package contains two top-level content areas:

1. `journal_upload/`: main manuscript source/PDF, Supplemental Material
   source/PDF, cover letter draft, bibliography, and included figure files.
2. `provenance/`: source-data CSV files, audit outputs, validation scripts,
   MATBG source modules, validation summaries, and provenance notes.

## Current Result

The current build records:

```text
manifest_entries = 77
copied_files = 80
status = pass
```

The copied-file count is larger than the manifest-entry count because the
builder also adds the manifest CSV, validation summary CSV, and repository
README to the provenance directory.

This is a checkpoint package for internal review and final-preparation work.
It is not a final journal upload until a fresh literature sweep is repeated at
submission time and the manuscript scope is confirmed.
