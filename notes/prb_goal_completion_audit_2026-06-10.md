# PRB Goal Completion Audit

Date: 2026-06-10

## Objective

Complete the major-revision work needed to bring the MATBG manuscript closer
to PRB publication standard and avoid recurrence of the first-round review
criticisms.

## Completion Boundary

The current deliverable is a local PRB major-revision response checkpoint.  It
does not include an APS Editorial Manager upload, a new absolute-stiffness
theory, or a device-level carrier-density calibration.

## Evidence Required

The checkpoint must contain:

1. revised main manuscript source and PDF,
2. revised Supplemental Material source and PDF,
3. PRB cover letter draft,
4. point-by-point response to reviewers,
5. pairing-family, robustness, and valley-sensitivity evidence packages,
6. table, scope, observable, evidence, submission-package, and checkpoint
   audits,
7. current manifest and local package build.

The machine-readable audit is:

```text
data/processed/prb_goal_completion_audit.csv
```

## Current Decision

The major-revision response checkpoint can be called complete only after
`scripts/run_prb_validation.py`, `scripts/build_prb_submission_package.py`, and
`scripts/audit_prb_submission_checkpoint.py` all pass on the current worktree.
