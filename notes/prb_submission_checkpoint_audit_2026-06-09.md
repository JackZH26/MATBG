# PRB Submission Checkpoint Audit

Date: 2026-06-09

## Purpose

This note records the final local checkpoint audit for the PRB-targeted
mechanism manuscript package.  It is intended to be run after the standard
validation chain and after the ignored local package has been built under
`submission/build/`.

The audit checks cross-file consistency that is broader than the mechanical
LaTeX/package smoke test: title alignment, required Jian Zhou authorship
metadata, declarations, cover letter signature, README workflow instructions,
validation summary status, manifest status, local package summary, package
directory contents, package zip contents, and the `submission/build/` ignore
rule.

## Command

```bash
python3 scripts/audit_prb_submission_checkpoint.py
```

Output:

```text
data/processed/prb_submission_checkpoint_audit.csv
```

## Current Scope

This is a local final-preparation checkpoint.  It does not make the package a
journal-ready upload by itself.  The final submission still requires a fresh
literature sweep at submission time and a final decision to keep the paper
within the normalized-response mechanism scope.

## Current Decision

Use the following sequence for a submission-facing local checkpoint:

```bash
python3 scripts/run_prb_validation.py
python3 scripts/build_prb_submission_package.py
python3 scripts/audit_prb_submission_checkpoint.py
```

The package should be rebuilt after any manuscript, Supplemental Material,
cover letter, validation-output, manifest, or audit-output change.
