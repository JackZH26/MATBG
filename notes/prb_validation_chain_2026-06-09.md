# PRB Validation Chain

Date: 2026-06-09

## Purpose

This note records the current one-command validation chain for the
PRB-targeted MATBG mechanism manuscript.

The chain is intentionally lightweight: it does not rerun expensive response
scans, but it verifies that the current manuscript, Supplemental Material,
processed tables, claim-scope boundaries, submission package structure, and
compiled PDFs remain internally consistent.

## Command

```bash
python3 scripts/run_prb_validation.py
```

Output:

```text
data/processed/prb_validation_summary.csv
```

## Current Result

All 12 validation checks pass.

The chain currently runs:

1. Python syntax compilation for all scripts in `scripts/`;
2. `scripts/audit_claim_scope.py`;
3. `scripts/audit_observable_policy.py`;
4. `scripts/audit_filling_sufficiency.py`;
5. `scripts/audit_convergence_sufficiency.py`;
6. `scripts/verify_manuscript_tables.py`;
7. `scripts/audit_submission_package.py`, including the PRB cover letter
   draft and required signature;
8. `scripts/build_prb_submission_manifest.py`, including the cover letter,
   included figures, key processed data tables, audit outputs, provenance
   notes, validation scripts, and MATBG source modules in the manuscript
   package inventory;
9. `latexmk` for the main manuscript;
10. `latexmk` for the Supplemental Material;
11. blocking-warning scan of the main LaTeX log;
12. blocking-warning scan of the Supplemental Material LaTeX log.

The log scans fail on undefined references, citation warnings, LaTeX errors,
and overfull boxes. They intentionally do not fail on the current benign
`nameref` and underfull-box warnings.

## Interpretation

This chain proves that the repository is internally consistent for the current
mechanism-paper scope. It does not prove that the manuscript is ready for
submission. A final PRB submission still requires a fresh literature sweep at
submission time and any explicit decision about whether to expand the scope to
absolute stiffness or device-level filling calibration.

## Current Decision

Use this command as the standard pre-commit and pre-submission smoke test for
the current manuscript package. Use
`scripts/build_prb_submission_package.py` after this chain when a local
checkpoint archive under `submission/build/` is needed, then run
`scripts/audit_prb_submission_checkpoint.py` for the final local
submission-facing consistency audit.
