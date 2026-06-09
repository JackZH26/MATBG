# Submission Package Audit

Date: 2026-06-09

## Purpose

This audit checks mechanical readiness of the current PRB manuscript package.
It complements the physics-facing claim-scope, observable-policy, convergence,
and filling audits by checking that the manuscript files, author blocks,
declarations, figures, labels, and submission-facing filenames remain
consistent.

## Command

```bash
python3 scripts/audit_submission_package.py
```

Output:

```text
data/processed/submission_package_audit.csv
```

## Current Result

All 59 submission-package checks pass.

The passing checks cover:

1. main manuscript and Supplemental Material `.tex` and `.pdf` files exist;
2. the main manuscript file names follow the
   `Zhou_<Full_Paper_Title_With_Underscores>_2026.tex/pdf` convention;
3. the main manuscript uses the APS/PRB RevTeX class;
4. main and Supplemental Material author blocks use `Jian Zhou`,
   `JZ Institute of Science, Hong Kong, China`, and `jack@jzis.org`;
5. prohibited author variants are absent from the paper files;
6. required declaration sections are present in both paper files;
7. required main-text and Supplemental Material sections are present;
8. current main figure and table labels are present;
9. current Supplemental Material table labels are present;
10. `\bibliography{references}` is used by both paper files;
11. every graphic included in the main manuscript exists in the repository.

## Interpretation

This audit does not prove that the paper is scientifically submission-ready.
It proves only that the current manuscript package satisfies a set of
mechanical and authorship invariants that should remain true during future
editing.  Scientific readiness still depends on the claim-scope guardrails,
finite-grid evidence, literature freshness, and any decision about whether to
expand the manuscript beyond the normalized-response mechanism scope.

## Current Decision

Keep this audit in the standard validation chain before future commits that
touch manuscript files, figure files, author blocks, declarations, or
submission package structure.
