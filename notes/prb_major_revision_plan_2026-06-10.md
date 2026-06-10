# PRB Major-Revision Plan

Date: 2026-06-10

Review source:
`/Users/jackzhou/Downloads/PRB_Review_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_MATBG_2026-06-10.md`

## Revision Goal

Revise the manuscript from a carefully scoped single-ansatz mechanism
checkpoint into a PRB-standard paper with explicit robustness evidence for the
normalized finite-band response signature.  The revision should prevent the
same first-round criticism from recurring: the claim must not depend only on a
single working orbital direction, a modest dense grid, one retained-band
truncation, or an under-audited valley-sewing convention.

## Review Diagnosis

The report recommends `Major Revision`.  The strongest criticism is not that
the present result is wrong, but that the claim-bearing observable remains too
internal to the current computational setup.  The present manuscript supports a
convention-sensitive normalized finite-band diagnostic.  A stronger PRB
revision needs to show whether that diagnostic survives changes in:

1. orbital pairing direction,
2. momentum grid,
3. retained-band truncation,
4. moire shell cutoff,
5. valley partner or sewing convention,
6. textual framing of normalized versus absolute stiffness observables.

## Work Package 1: Pairing-Family Analysis

Purpose: answer whether `M1=taux_sigmax` is representative of an
interband-capable orbital pairing family, or a special ansatz.

First-pass candidate family:

```text
taux_sigmax
taux_sigma0
tau0_sigmaz
tauz_sigmaz
tau0_sigmax
taux_sigmaz
tauz_sigma0
tauz_sigmax
```

Current artifacts:

```text
configs/pairing_family_response_scan.yaml
scripts/run_pairing_family_response_scan.py
scripts/plot_pairing_family_response.py
data/processed/pairing_family_response_scan.csv
data/processed/pairing_family_response_summary.csv
figures/pairing_family_response_summary.png
figures/pairing_family_response_summary.pdf
notes/pairing_family_major_revision_result_2026-06-10.md
```

Acceptance target for a stronger PRB claim: the positive fixed-Frobenius signal
should appear across more than one symmetry-allowed interband-capable orbital
direction, while the fixed-Delta0 control remains weak enough to demonstrate
normalization dependence rather than an unconditional stiffness enhancement.

## Work Package 2: Grid, Truncation, and Shell Robustness

Purpose: answer the reviewer's numerical robustness criticism.

Planned scan axes:

```text
nk:       9, 11, 13, 15, optionally 17
n_keep:   4, 6, 8
n_shell:  2, 3, 4
mu:      -4, -2, 0, 2, 4 meV
eta:      0, 0.5, 1
```

Planned artifacts:

```text
configs/prb_major_revision_robustness.yaml
scripts/run_prb_major_revision_robustness.py
scripts/audit_prb_major_revision_robustness.py
data/processed/prb_major_revision_robustness_matrix.csv
data/processed/prb_major_revision_robustness_summary.csv
data/processed/prb_major_revision_robustness_audit.csv
figures/prb_major_revision_robustness_matrix.png
figures/prb_major_revision_robustness_matrix.pdf
notes/prb_major_revision_robustness_audit_2026-06-10.md
```

Decision rule: if the signal is stable under the main grid/truncation/shell
changes, the main text can state a robust finite-band normalized-response
signature.  If it is not stable, the conclusion must remain a narrower
diagnostic-framework result.

## Work Package 3: Valley-Sewing Sensitivity

Purpose: convert the current valley-sewing caveat into a quantitative
sensitivity test.

Planned comparisons:

```text
tr_sewn
conjugate_k
same_valley
sewn_time_reversed_valley
```

The projection-level diagnostics already support these partner conventions in
`scripts/run_bm_pairing_projection_gate.py`.  The response-scan layer should be
extended so selected key points can be recomputed under alternative partner
choices.

Planned artifacts:

```text
configs/valley_sewing_response_sensitivity.yaml
scripts/run_valley_sewing_response_sensitivity.py
scripts/audit_valley_sewing_response_sensitivity.py
data/processed/valley_sewing_response_sensitivity.csv
data/processed/valley_sewing_response_sensitivity_summary.csv
data/processed/valley_sewing_response_sensitivity_audit.csv
figures/valley_sewing_response_sensitivity.png
figures/valley_sewing_response_sensitivity.pdf
notes/valley_sewing_response_sensitivity_2026-06-10.md
```

## Work Package 4: Manuscript Reframing

After Work Packages 1-3 produce stable evidence, revise the paper text:

1. Add a sharper physical interpretation of the normalized diagnostic.
2. Explain what fixed-Frobenius normalization holds fixed and why the diagnostic
   is still physically informative.
3. Present fixed-Delta0 as a central control, not a secondary caveat.
4. Add a pairing-family result figure or table.
5. Move or compress the absolute-unit benchmark audit in the main text, unless
   a stronger absolute convention is completed.
6. Strengthen captions warning that `nu_proxy` is not a calibrated experimental
   filling.
7. Strengthen the data-availability statement with repository, commit, and
   reproduction-command information.

## Work Package 5: Validation and Response Package

Before calling the revised manuscript PRB-ready:

1. Update manuscript and Supplemental Material tables from CSV evidence.
2. Update claim-scope, observable-policy, convergence, filling, and package
   audits so they cover the new revision evidence.
3. Rebuild the main PDF and Supplemental Material PDF.
4. Rebuild the PRB package manifest and checkpoint package.
5. Write a point-by-point response matrix to the review report.

## Current Revision Decision

Do not strengthen the abstract or conclusion yet.  The first three
major-revision evidence layers are now in place: the pairing-family scan, a
core `nk/n_keep/n_shell` robustness matrix, and a valley-sewing response
sensitivity diagnostic.  The robustness matrix supports a stronger
production-scope statement for `n_keep=6,8`, but it also reveals a
low-truncation boundary at `n_keep=4`, `mu=-4 meV` that must be disclosed.  The
valley-sewing diagnostic shows that the positive response is stable within the
declared `tr_sewn` convention, while alternative partner choices are
sign-sensitive and can break the finite-band BdG particle-hole diagnostic.
The manuscript can now be rewritten, but the revised conclusion must remain
scoped to the declared finite-band diagnostic convention rather than claiming
valley-basis-independent stiffness physics.
