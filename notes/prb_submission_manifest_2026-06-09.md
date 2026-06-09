# PRB Submission Manifest

Date: 2026-06-09

## Purpose

This note describes the current manifest for the PRB-targeted MATBG mechanism
manuscript package.

The manifest is not a journal upload archive. It is a deterministic inventory
of the files that constitute the current manuscript checkpoint: main text,
Supplemental Material, bibliography, included figures, key source-data CSV
files, audit outputs, validation scripts, and provenance notes.

## Command

```bash
python3 scripts/build_prb_submission_manifest.py
```

Output:

```text
data/processed/prb_submission_manifest.csv
```

## Current Scope

The manifest covers the current normalized-response mechanism-paper scope. It
does not include files for an expanded direct experimental-comparison paper,
because the current manuscript intentionally does not make claim-bearing
absolute stiffness or device-calibrated filling predictions.

## Current Decision

Use this manifest as the working inventory before creating any eventual journal
upload archive. A final submission-time package should be regenerated after
the final literature sweep and after deciding whether the manuscript remains
within the present normalized-response mechanism scope.
