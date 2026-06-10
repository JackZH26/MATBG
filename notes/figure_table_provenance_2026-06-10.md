# Figure and Table Provenance

Date: 2026-06-10

Manuscript:
`Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex`

Supplement:
`Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_Supplemental_Material_2026.tex`

## Purpose

This note records the current manuscript-facing figure and table provenance
after the major-revision response package.  It supersedes the 2026-06-09
provenance note for the active manuscript because the revised paper now
includes pairing-family, grid/truncation/shell robustness, and valley-partner
response-sensitivity evidence.

## Global Production Scope

Unless an entry states otherwise, the production mechanism scans use:

```text
theta_deg = 1.05
vF_eV_A = 2.135
w0_meV = 87.2
w1_meV = 109.0
n_shell = 3
n_keep = 6
delta0_meV = 1.0
velocity_dk_Ainv = 1.0e-6
partner_convention = tr_sewn
m0 = tau0_sigma0
m1 = taux_sigmax
normalizations = fixed_frobenius_norm, fixed_delta0
```

The major-revision scans deliberately extend this scope as stress tests:

```text
pairing family: 8 orbital directions at nk=7
robustness matrix: nk=9,11,13,15; n_keep=4,6,8; N_shell=2,3,4
valley sensitivity: tr_sewn and three alternative partner conventions
```

## Main Figures

| Label | Output | Source data | Script |
|---|---|---|---|
| `fig:workflow` | `figures/workflow_schematic_prb.png` | workflow definitions | `scripts/plot_workflow_schematic.py` |
| `fig:heatmap_frob` | `figures/mu_eta_heatmap_nk7_nkeep6_fixed_frobenius.png` | `data/processed/mu_eta_response_scan_nk7_nkeep6.csv` | `scripts/plot_mu_eta_heatmap.py` |
| `fig:heatmap_delta0` | `figures/mu_eta_heatmap_nk7_nkeep6_fixed_delta0.png` | `data/processed/mu_eta_response_scan_nk7_nkeep6.csv` | `scripts/plot_mu_eta_heatmap.py` |

Each manuscript figure has a matching PDF or PNG copy in `figures/`, and
included graphics are checked by `scripts/audit_submission_package.py`.

## Main Tables

| Label | Content | Source data | Verification |
|---|---|---|---|
| `tab:dense_eta` | dense `mu` scan at `nk=7`, `n_keep=6` | `data/processed/mu_eta_response_scan_nk7_nkeep6_eta1_summary.csv` | `scripts/verify_manuscript_tables.py` |
| `tab:nk9` | selected `nk=9` key-point validation | `data/processed/mu_response_scan_nk9_nkeep6_keypoints_summary.csv` | `scripts/verify_manuscript_tables.py` |
| `tab:prb_audit` | historical PRB benchmark reconstruction audit | reconstruction CSVs listed in the 2026-06-09 note | `scripts/verify_manuscript_tables.py` |
| `tab:major_revision_evidence` | pairing-family, robustness, and valley-sensitivity evidence summary | 2026-06-10 processed CSVs below | `scripts/verify_manuscript_tables.py` |

## Major-Revision Evidence

### Pairing Family

Artifacts:

```text
configs/pairing_family_response_scan.yaml
scripts/run_pairing_family_response_scan.py
scripts/audit_pairing_family_response.py
scripts/plot_pairing_family_response.py
data/processed/pairing_family_response_scan.csv
data/processed/pairing_family_response_summary.csv
data/processed/pairing_family_response_audit.csv
figures/pairing_family_response_summary.pdf
figures/pairing_family_response_summary.png
notes/pairing_family_major_revision_result_2026-06-10.md
```

Reproduction:

```bash
python3 scripts/run_pairing_family_response_scan.py
python3 scripts/audit_pairing_family_response.py
python3 scripts/plot_pairing_family_response.py
```

Manuscript use:

```text
tab:major_revision_evidence
fig:sm_pairing_family_revision
tab:sm_pairing_family_revision
```

### Grid, Truncation, and Shell Robustness

Artifacts:

```text
configs/prb_major_revision_robustness.yaml
scripts/run_prb_major_revision_robustness.py
scripts/audit_prb_major_revision_robustness.py
scripts/plot_prb_major_revision_robustness.py
data/processed/prb_major_revision_robustness_matrix.csv
data/processed/prb_major_revision_robustness_summary.csv
data/processed/prb_major_revision_robustness_audit.csv
figures/prb_major_revision_robustness_matrix.pdf
figures/prb_major_revision_robustness_matrix.png
notes/prb_major_revision_robustness_audit_2026-06-10.md
```

Reproduction:

```bash
python3 scripts/run_prb_major_revision_robustness.py
python3 scripts/audit_prb_major_revision_robustness.py
python3 scripts/plot_prb_major_revision_robustness.py
```

Manuscript use:

```text
tab:major_revision_evidence
fig:sm_major_revision_robustness
tab:sm_major_revision_robustness
```

### Valley-Partner Response Sensitivity

Artifacts:

```text
configs/valley_sewing_response_sensitivity.yaml
scripts/run_valley_sewing_response_sensitivity.py
scripts/audit_valley_sewing_response_sensitivity.py
scripts/plot_valley_sewing_response_sensitivity.py
data/processed/valley_sewing_response_sensitivity.csv
data/processed/valley_sewing_response_sensitivity_summary.csv
data/processed/valley_sewing_response_sensitivity_audit.csv
figures/valley_sewing_response_sensitivity.pdf
figures/valley_sewing_response_sensitivity.png
notes/valley_sewing_response_sensitivity_2026-06-10.md
```

Reproduction:

```bash
python3 scripts/run_valley_sewing_response_sensitivity.py
python3 scripts/audit_valley_sewing_response_sensitivity.py
python3 scripts/plot_valley_sewing_response_sensitivity.py
```

Manuscript use:

```text
tab:major_revision_evidence
fig:sm_valley_response_sensitivity
tab:sm_valley_response_sensitivity
```

## Supplemental Tables

The Supplemental Material contains the following CSV-backed tables:

| Label | Source data | Verification |
|---|---|---|
| `tab:sm_filling_crosswalk` | `data/processed/filling_crosswalk_nk7_nshell3.csv` | `scripts/verify_manuscript_tables.py` |
| `tab:sm_filling_sufficiency` | `data/processed/filling_sufficiency_audit.csv` | `scripts/verify_manuscript_tables.py` |
| `tab:sm_valley_sewing` | `data/processed/valley_sewing_diagnostic.csv` | `scripts/verify_manuscript_tables.py` |
| `tab:sm_valley_response_sensitivity` | `data/processed/valley_sewing_response_sensitivity_summary.csv` | `scripts/verify_manuscript_tables.py` |
| `tab:sm_pairing_family_revision` | `data/processed/pairing_family_response_summary.csv` | `scripts/verify_manuscript_tables.py` |
| `tab:sm_nk_convergence` | `data/processed/mu_response_scan_nk9_nkeep6_keypoints_summary.csv`, `data/processed/mu_response_scan_nk11_nkeep6_keypoints_summary.csv`, `data/processed/mu_response_scan_nk13_nkeep6_keypoints_summary.csv` | `scripts/verify_manuscript_tables.py` |
| `tab:sm_nk_trend` | `data/processed/nk_trend_audit_nkeep6.csv` | `scripts/verify_manuscript_tables.py` |
| `tab:sm_nk15` | `data/processed/mu_response_scan_nk15_nkeep6_spotcheck_summary.csv` | `scripts/verify_manuscript_tables.py` |
| `tab:sm_convergence_sufficiency` | `data/processed/convergence_sufficiency_audit.csv` | `scripts/verify_manuscript_tables.py` |
| `tab:sm_major_revision_robustness` | `data/processed/prb_major_revision_robustness_summary.csv` | `scripts/verify_manuscript_tables.py` |

Interpretive tables without direct numerical CSV dependencies are guarded by
text audits:

```text
tab:sm_reporting_layers
tab:sm_provenance
tab:sm_claim_scope
```

Guardrail scripts:

```bash
python3 scripts/audit_claim_scope.py
python3 scripts/audit_observable_policy.py
python3 scripts/audit_submission_package.py
```

## Final Validation Command

The active one-command validation chain is:

```bash
python3 scripts/run_prb_validation.py
```

It runs the manuscript table verifier, the scope and observable audits, the
major-revision evidence audits, LaTeX builds, log scans, and manifest
construction.
