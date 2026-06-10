# PRB Validation Chain

Date: 2026-06-10

Run:

```bash
python3 scripts/run_prb_validation.py
```

The command writes:

```text
data/processed/prb_validation_summary.csv
data/processed/prb_submission_manifest.csv
```

The 2026-06-10 validation chain covers:

1. syntax compilation for all repository scripts,
2. claim-scope and observable-policy audits,
3. filling-sufficiency and convergence-sufficiency audits,
4. pairing-family response audit,
5. grid/truncation/shell major-revision robustness audit,
6. valley-partner response-sensitivity audit,
7. manuscript and Supplemental Material table verification against CSV data,
8. submission-package mechanical audit,
9. submission-manifest construction,
10. main and Supplemental Material LaTeX builds,
11. blocking LaTeX log scans.

This validation chain is local evidence for the major-revision response
package. It is not a substitute for the author's final scientific review or
for the journal upload workflow.
