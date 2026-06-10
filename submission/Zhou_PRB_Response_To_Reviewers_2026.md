# Response to Referee Report

Date: June 10, 2026

Manuscript: "Interband Pairing Signatures in the Superfluid Response of Magic-Angle Twisted Bilayer Graphene"

Author: Jian Zhou

Recommendation addressed: Major Revision

Dear Editors and Referee,

Thank you for the careful and constructive report.  I have revised the
manuscript as a major-revision response package rather than treating the first
version as merely requiring minor textual clarification.  The revised paper now
adds three new evidence layers: a pairing-family scan, a grid, truncation, and
shell robustness matrix, and a response-level valley-partner sensitivity audit.
The main text and Supplemental Material have also been reframed so that the
claim remains a normalized finite-band diagnostic result, not an absolute
stiffness prediction.

No valley-basis-independent absolute stiffness claim is made.  The revised
conclusion is intentionally scoped to the declared `tr_sewn` finite-band
diagnostic convention, with the remaining boundaries stated explicitly.

## Summary of Major Changes

1. Added a pairing-family analysis across eight real, symmetric, Hermitian
   orbital directions.  The fixed-Frobenius signal is positive in 32/32
   pairing-family rows, with a response range of +6.43% to +9.49%.

2. Added a grid/truncation/shell robustness matrix over `nk=9,11,13,15`,
   `n_keep=4,6,8`, `N_shell=2,3,4`, five chemical potentials, and three eta
   values.  The production and expanded truncations `n_keep>=6` are positive
   in 120/120 fixed-Frobenius rows; the disclosed low-truncation boundary is
   confined to `n_keep=4`, `mu=-4 meV`.

3. Added a response-level valley-partner sensitivity audit.  The production
   `tr_sewn` convention remains positive in 24/24 fixed-Frobenius rows with
   zero particle-hole spectrum error, while alternative partner choices are
   sign-sensitive and show measurable particle-hole errors.

4. Updated the Abstract, Results, Discussion, Conclusions, Supplemental
   Material, table verifier, claim-scope audit, observable-policy audit,
   package manifest, and validation chain so that the new evidence is included
   in the reproducible manuscript package.

## Point-by-Point Response

### Major Concern 1: The claim-bearing observable remains too internal

I agree that the normalized response ratio must not be presented as a direct
experimental stiffness prediction.  The revised manuscript now states more
prominently that normalized response ratios are the claim-bearing quantities
and that raw finite-band response values remain diagnostic units.

Changes made:

- Main text: Abstract, Results, Discussion, Conclusions, and Declarations/Data
  availability now frame the central result as a normalized finite-band
  diagnostic.
- Supplemental Material: the reporting-layers table and claim-scope table now
  separate raw diagnostics, normalized ratios, benchmark-unit audits, and
  excluded absolute-stiffness interpretations.
- Audit evidence: `scripts/audit_observable_policy.py` passes 12/12 checks.

### Major Concern 2: Dependence on normalization convention

I agree that the fixed-Frobenius and fixed-Delta0 contrast is central rather
than a peripheral caveat.  The revised text now treats fixed-Delta0 as a
control result throughout.

Changes made:

- Main text: the Abstract and Results state that fixed-Frobenius is the
  claim-bearing comparison while fixed-Delta0 is weak or sign-sensitive.
- Supplemental Material: the pairing-family and robustness tables report both
  fixed-Frobenius and fixed-Delta0 behavior.
- Audit evidence: `scripts/verify_manuscript_tables.py` checks the reported
  values against the processed CSV files.

### Major Concern 3: Single working direction `M1=taux_sigmax`

I agree that the first version over-relied on one working orbital direction.
The revised manuscript adds a pairing-family scan over eight interband-capable
orbital directions.

Evidence added:

- Config: `configs/pairing_family_response_scan.yaml`
- Scripts: `scripts/run_pairing_family_response_scan.py`,
  `scripts/audit_pairing_family_response.py`, and
  `scripts/plot_pairing_family_response.py`
- Data: `data/processed/pairing_family_response_scan.csv` and
  `data/processed/pairing_family_response_summary.csv`
- Figure: `figures/pairing_family_response_summary.pdf`
- Supplemental label: `tab:sm_pairing_family_revision`

Result:

- Fixed-Frobenius: 32/32 positive rows, +6.43% to +9.49%.
- Fixed-Delta0: weaker and sign-sensitive, -1.46% to +2.91%.

### Major Concern 4: Numerical convergence and truncation control

I agree that the previous `nk=7`, `n_keep=6` dense map was not enough by itself
for a PRB-strength robustness claim.  The revised manuscript adds a rectangular
robustness matrix spanning grid, retained-band truncation, and moire-shell
cutoff.

Evidence added:

- Config: `configs/prb_major_revision_robustness.yaml`
- Scripts: `scripts/run_prb_major_revision_robustness.py`,
  `scripts/audit_prb_major_revision_robustness.py`, and
  `scripts/plot_prb_major_revision_robustness.py`
- Data: `data/processed/prb_major_revision_robustness_matrix.csv` and
  `data/processed/prb_major_revision_robustness_summary.csv`
- Figure: `figures/prb_major_revision_robustness_matrix.pdf`
- Main label: `tab:major_revision_evidence`
- Supplemental label: `tab:sm_major_revision_robustness`

Result:

- All rows: 172/180 fixed-Frobenius rows positive.
- Production and expanded truncations `n_keep>=6`: 120/120 positive.
- Production scope `n_keep>=6`, `N_shell>=3`: 80/80 positive.
- Boundary retained: `n_keep=4`, `mu=-4 meV` can be negative.

### Major Concern 5: Valley-sewing treatment

I agree that valley sewing is part of the physics interpretation rather than a
minor technicality.  The revised manuscript now treats the valley convention as
a quantitative boundary condition.

Evidence added:

- Config: `configs/valley_sewing_response_sensitivity.yaml`
- Scripts: `scripts/run_valley_sewing_response_sensitivity.py`,
  `scripts/audit_valley_sewing_response_sensitivity.py`, and
  `scripts/plot_valley_sewing_response_sensitivity.py`
- Data: `data/processed/valley_sewing_response_sensitivity.csv` and
  `data/processed/valley_sewing_response_sensitivity_summary.csv`
- Figure: `figures/valley_sewing_response_sensitivity.pdf`
- Supplemental label: `tab:sm_valley_response_sensitivity`

Result:

- `tr_sewn`: 24/24 positive fixed-Frobenius rows, +4.37% to +13.60%, zero
  particle-hole spectrum error.
- Alternative partner choices: sign-sensitive, with nonzero particle-hole
  spectrum errors.

The revised conclusion therefore does not claim valley-basis-independent
stiffness physics.

### Major Concern 6: Distinction from existing literature

The revised manuscript sharpens the novelty claim: the pairing object is
defined in orbital space, projected into the band basis, and tested under
normalization controls.  The paper now emphasizes that this provides a
reproducible diagnostic for how orbital-defined interband structure enters a
finite-band response calculation, while avoiding an overclaim of universal
stiffness enhancement.

Changes made:

- Introduction and Discussion now state the distinction between orbital-first
  construction and band-basis off-diagonal diagnostics.
- Data availability now points to the public repository and reproducible CSV,
  script, and figure artifacts.

## Minor Concerns

### Filling proxy readability

The figure and table language has been tightened.  `nu_proxy` remains a scan
label and is not presented as calibrated device filling.  The Supplemental
Material preserves the central-flat-band crosswalk and the filling-sufficiency
audit.

### Workflow emphasis

The Results section now moves more directly from the workflow schematic to the
claim-bearing dense response table, heatmaps, and major-revision evidence
table.

### Data availability

The data availability statement now names the repository:

`https://github.com/JackZH26/MATBG`

The manifest, CSV outputs, scripts, configs, and figures are included in the
local submission checkpoint package.

### Absolute-unit audit

The absolute-unit material remains a boundary and provenance audit rather than
a claim-bearing result.  The revised manuscript uses it only to explain why
absolute experimental stiffness comparison is deferred.

## Validation Record

The revised package is checked by:

```text
python3 scripts/run_prb_validation.py
python3 scripts/build_prb_submission_package.py
python3 scripts/audit_prb_submission_checkpoint.py
```

The current validation chain includes script syntax checks, manuscript table
verification, claim-scope and observable-policy audits, filling and convergence
sufficiency audits, the three new major-revision evidence audits, LaTeX builds,
log checks, manifest construction, local package construction, and package
hash-consistency checks.

Sincerely,
Jian Zhou
Principal Investigator
JZ Institute of Science, Hong Kong, China
jack@jzis.org
