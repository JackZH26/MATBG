# PRB Submission Checkpoint Audit Note

Date: 2026-06-10

The final local checkpoint audit is:

```bash
python3 scripts/audit_prb_submission_checkpoint.py
```

The machine-readable output is:

```text
data/processed/prb_submission_checkpoint_audit.csv
```

The 2026-06-10 audit checks:

1. title consistency across main text, supplement, cover letter, response
   letter, and README,
2. required Jian Zhou authorship metadata and signature blocks,
3. required declarations,
4. README commands for validation, package build, and final checkpoint audit,
5. validation-summary coverage of the three new major-revision audits,
6. manifest presence and required major-revision artifact IDs,
7. local package directory and zip contents,
8. SHA-256 consistency between manifest-tracked files and packaged copies.

This audit is local.  It does not perform an APS Editorial Manager upload.
