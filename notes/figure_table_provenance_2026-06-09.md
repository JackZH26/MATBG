# Figure and Table Provenance

Date: 2026-06-09

Manuscript:
`Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex`

## Purpose

This manifest records the data, scripts, configs, and reproduction commands
behind every figure and table currently used in the PRB draft. It is intended
to support the standalone Supplemental Material reproducibility section in
`Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_Supplemental_Material_2026.tex`.

## Global Model Parameters

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

Primary config file:
`configs/mu_eta_dense_scan.yaml`.

## Dense Mu-Eta Response Data

Source CSV:
`data/processed/mu_eta_response_scan_nk7_nkeep6.csv`

Summary CSV:
`data/processed/mu_eta_response_scan_nk7_nkeep6_eta1_summary.csv`

Reproduction commands:

```bash
python3 scripts/run_mu_response_scan.py \
  --nk 7 \
  --n-shell 3 \
  --n-keep 6 \
  --mus -5 -4 -3 -2 -1 0 1 2 3 4 5 \
  --etas 0 0.25 0.5 0.75 1 \
  --output data/processed/mu_eta_response_scan_nk7_nkeep6.csv

python3 scripts/summarize_eta_effect.py \
  data/processed/mu_eta_response_scan_nk7_nkeep6.csv \
  --output data/processed/mu_eta_response_scan_nk7_nkeep6_eta1_summary.csv
```

Note: the dense scan currently reuses `scripts/run_mu_response_scan.py` with
explicit dense `--mus` and `--etas` values. There is no separate dense-run
script yet.

## Manuscript Figures

| Label | Output | Source data | Script | Reproduction command | Status |
|---|---|---|---|---|---|
| `fig:heatmap_frob` | `figures/mu_eta_heatmap_nk7_nkeep6_fixed_frobenius.png` | `data/processed/mu_eta_response_scan_nk7_nkeep6.csv` | `scripts/plot_mu_eta_heatmap.py` | `python3 scripts/plot_mu_eta_heatmap.py --input data/processed/mu_eta_response_scan_nk7_nkeep6.csv --normalization fixed_frobenius_norm --output figures/mu_eta_heatmap_nk7_nkeep6_fixed_frobenius.png` | Reproducible |
| `fig:heatmap_delta0` | `figures/mu_eta_heatmap_nk7_nkeep6_fixed_delta0.png` | `data/processed/mu_eta_response_scan_nk7_nkeep6.csv` | `scripts/plot_mu_eta_heatmap.py` | `python3 scripts/plot_mu_eta_heatmap.py --input data/processed/mu_eta_response_scan_nk7_nkeep6.csv --normalization fixed_delta0 --output figures/mu_eta_heatmap_nk7_nkeep6_fixed_delta0.png` | Reproducible |

Each plot command also writes the matching PDF next to the PNG.

## Manuscript Tables

### `tab:dense_eta`

Manuscript content:
dense `mu` scan comparing `eta=1` to `eta=0` for `nk=7`, `n_keep=6`.

Data source:
`data/processed/mu_eta_response_scan_nk7_nkeep6_eta1_summary.csv`

Rows used:

```text
normalization = fixed_frobenius_norm
normalization = fixed_delta0
mu_meV = -5, -4, ..., 5
eta_baseline = 0
eta_target = 1
```

Columns mapped into LaTeX:

```text
mu_meV -> mu column
nu_proxy -> nu_proxy column
D_iso_rel_target_vs_baseline where normalization=fixed_frobenius_norm
  -> fixed Frobenius column
D_iso_rel_target_vs_baseline where normalization=fixed_delta0
  -> fixed Delta0 column
```

Current status:
values are copied from the summary CSV and rounded in the LaTeX table. The
rounding is checked by `scripts/verify_manuscript_tables.py`.

### `tab:sm_reporting_layers`

Supplemental content:
qualitative reporting convention separating raw finite-band diagnostics,
normalized mechanism ratios, eV A^2 per-flavor benchmark audit values, and the
retained-band filling proxy.

Source:
`notes/normalization_and_units_strategy.md`
and `notes/observable_policy_decision_2026-06-09.md`

Current status:
this table has no numerical CSV dependencies. It records interpretive
boundaries for the manuscript and is not part of the numerical table verifier.
The text-level policy is checked by `scripts/audit_observable_policy.py`.

### `tab:sm_filling_crosswalk`

Supplemental content:
crosswalk between the retained-band filling proxy and central two-flat-band
filling for the dense `nk=7`, `n_keep=6` scan.

Data source:
`data/processed/filling_crosswalk_nk7_nshell3.csv`

Script:
`scripts/build_filling_crosswalk.py`

Reproduction command:

```bash
python3 scripts/build_filling_crosswalk.py
```

Columns mapped into LaTeX:

```text
mu_meV -> mu column
nu_proxy -> nu_proxy column
nu_flat -> nu_flat column
flat_occupied_bands_per_flavor -> occupied flat bands/flavor column
```

Current status:
values are generated from the BM central-pair spectrum and checked by
`scripts/verify_manuscript_tables.py`.

### Text-Level Claim and Observable Audits

Outputs:

```text
data/processed/claim_scope_audit.csv
data/processed/observable_policy_audit.csv
```

Scripts:

```bash
python3 scripts/audit_claim_scope.py
python3 scripts/audit_observable_policy.py
```

Current status:
these audits are guardrails for manuscript scope and observable policy. They do
not replace numerical verification, but they check that the current draft does
not promote finite-band diagnostics to claim-bearing absolute stiffness values.

### `tab:nk9`

Manuscript content:
selected `nk=9`, `n_keep=6` validation values for `eta=1` relative to `eta=0`.

Source CSV:
`data/processed/mu_response_scan_nk9_nkeep6_keypoints.csv`

Summary CSV:
`data/processed/mu_response_scan_nk9_nkeep6_keypoints_summary.csv`

Reproduction commands:

```bash
python3 scripts/run_mu_response_scan.py \
  --nk 9 \
  --n-shell 3 \
  --n-keep 6 \
  --mus -4 0 2 4 \
  --etas 0 0.5 1 \
  --output data/processed/mu_response_scan_nk9_nkeep6_keypoints.csv

python3 scripts/summarize_eta_effect.py \
  data/processed/mu_response_scan_nk9_nkeep6_keypoints.csv \
  --output data/processed/mu_response_scan_nk9_nkeep6_keypoints_summary.csv
```

Columns mapped into LaTeX:

```text
mu_meV -> mu column
D_iso_rel_target_vs_baseline where normalization=fixed_frobenius_norm
  -> fixed Frobenius column
D_iso_rel_target_vs_baseline where normalization=fixed_delta0
  -> fixed Delta0 column
```

Current status:
values are copied from the summary CSV and rounded in the LaTeX table. The
rounding is checked by `scripts/verify_manuscript_tables.py`.

### Supplemental `nk=9/11/13` key-point convergence figure and table

Supplemental content:
selected `nk=9`, `nk=11`, and `nk=13` validation values for `eta=1` relative
to `eta=0`.

Figure files:
`figures/nk_convergence_keypoints_nkeep6.png`
`figures/nk_convergence_keypoints_nkeep6.pdf`

Source CSV:
`data/processed/mu_response_scan_nk11_nkeep6_keypoints.csv`
`data/processed/mu_response_scan_nk13_nkeep6_keypoints.csv`

Summary CSV:
`data/processed/mu_response_scan_nk11_nkeep6_keypoints_summary.csv`
`data/processed/mu_response_scan_nk13_nkeep6_keypoints_summary.csv`

Reproduction commands:

```bash
python3 scripts/run_mu_response_scan.py \
  --nk 11 \
  --n-shell 3 \
  --n-keep 6 \
  --mus -4 0 2 4 \
  --etas 0 0.5 1 \
  --output data/processed/mu_response_scan_nk11_nkeep6_keypoints.csv

python3 scripts/summarize_eta_effect.py \
  data/processed/mu_response_scan_nk11_nkeep6_keypoints.csv \
  --output data/processed/mu_response_scan_nk11_nkeep6_keypoints_summary.csv

python3 scripts/run_mu_response_scan.py \
  --nk 13 \
  --n-shell 3 \
  --n-keep 6 \
  --mus -4 0 2 4 \
  --etas 0 0.5 1 \
  --output data/processed/mu_response_scan_nk13_nkeep6_keypoints.csv

python3 scripts/summarize_eta_effect.py \
  data/processed/mu_response_scan_nk13_nkeep6_keypoints.csv \
  --output data/processed/mu_response_scan_nk13_nkeep6_keypoints_summary.csv

python3 scripts/plot_nk_convergence_keypoints.py
```

Config:
`configs/mu_response_convergence_nk11.yaml`
`configs/mu_response_convergence_nk13.yaml`

Current status:
the fixed-Frobenius response remains positive at all four key points and all
three checked grids. The Supplemental Material table values are checked by
`scripts/verify_manuscript_tables.py` against the `nk=9`, `nk=11`, and `nk=13`
summary CSV files. The Supplemental Material figure is generated from the same
summary CSV files.

### Supplemental finite-grid trend audit figure and table

Supplemental content:
finite-grid trend audit using the selected `nk=9`, `nk=11`, and `nk=13`
key-point summaries.  The plotted trend coordinate is `1/nk^2`, with `1/nk`
stored as a sensitivity check in the CSV and table.

Figure files:
`figures/nk_trend_audit_nkeep6.png`
`figures/nk_trend_audit_nkeep6.pdf`

Source CSV:
`data/processed/nk_trend_audit_nkeep6.csv`

Script:
`scripts/analyze_nk_trend.py`

Reproduction command:

```bash
python3 scripts/analyze_nk_trend.py
```

Config:
`configs/nk_trend_audit.yaml`

Columns mapped into LaTeX:

```text
min_percent -> min column
max_percent -> max column
intercept_percent_h2 -> 1/nk^2 intercept column
intercept_percent_h1 -> 1/nk intercept column
measured_sign_status -> sign column
```

Current status:
values are generated from the `nk=9/11/13` summary CSV files and checked by
`scripts/verify_manuscript_tables.py`.

### Supplemental nk15 spot-check table

Supplemental content:
targeted `nk=15` spot check at `mu=0,2` meV, comparing `eta=1` to `eta=0` for
fixed-Frobenius and fixed-Delta0 normalization.

Source CSV:
`data/processed/mu_response_scan_nk15_nkeep6_spotcheck.csv`
`data/processed/mu_response_scan_nk15_nkeep6_spotcheck_summary.csv`

Reproduction commands:

```bash
python3 scripts/run_mu_response_scan.py \
  --nk 15 \
  --n-shell 3 \
  --n-keep 6 \
  --mus 0 2 \
  --etas 0 1 \
  --output data/processed/mu_response_scan_nk15_nkeep6_spotcheck.csv

python3 scripts/summarize_eta_effect.py \
  data/processed/mu_response_scan_nk15_nkeep6_spotcheck.csv \
  --output data/processed/mu_response_scan_nk15_nkeep6_spotcheck_summary.csv
```

Config:
`configs/mu_response_spotcheck_nk15.yaml`

Columns mapped into LaTeX:

```text
nk13 D_iso_rel_target_vs_baseline -> nk=13 column
nk15 D_iso_rel_target_vs_baseline -> nk=15 column
nk15 - nk13 -> 15-13 column
nk15 W_inter_target -> W_inter(15) column
```

Current status:
values are checked by `scripts/verify_manuscript_tables.py`.

### Supplemental convergence-sufficiency self-audit table

Supplemental content:
manuscript-level convergence sufficiency checks combining the selected
`nk=9/11/13` key-point data, finite-grid trend audit, targeted `nk=15` spot
check, fixed-Delta0 control, and `W_inter` grid stability.

Source CSV:
`data/processed/convergence_sufficiency_audit.csv`

Script:
`scripts/audit_convergence_sufficiency.py`

Reproduction command:

```bash
python3 scripts/audit_convergence_sufficiency.py
```

Columns mapped into LaTeX:

```text
check_id -> check column after manuscript-facing relabeling
measured_value -> measured value column
consequence -> manuscript consequence column
```

Current status:
the audit passes all nine checks. The Supplemental Material table values are
checked by `scripts/verify_manuscript_tables.py`.

### Supplemental claim-scope audit table

Supplemental content:
qualitative table separating allowed normalized-response mechanism claims from
excluded interpretations such as direct experimental stiffness agreement,
device-level carrier-density calibration, or final continuum-limit estimates.

Source CSV:
`data/processed/claim_scope_audit.csv`

Script:
`scripts/audit_claim_scope.py`

Reproduction command:

```bash
python3 scripts/audit_claim_scope.py
```

Config:
`configs/claim_scope_audit.yaml`

Current status:
the script checks required conservative boundary phrases in the main text and
Supplemental Material, checks for a short list of forbidden overclaims, and
records the result as a CSV guardrail for future edits.

### Supplemental raw valley sewing diagnostic table

Supplemental content:
diagnostic comparison between independently diagonalized valley-minus
eigenvectors at `-k` and the time-reversal-sewn target `U_plus(k)^*`.

Source CSV:
`data/processed/valley_sewing_diagnostic.csv`

Reproduction command:

```bash
python3 scripts/run_valley_sewing_diagnostic.py \
  --n-shell 3 \
  --nk 3 \
  --n-keep-values 2 4 6 \
  --output data/processed/valley_sewing_diagnostic.csv
```

Config:
`configs/valley_sewing_diagnostic.yaml`

Current status:
raw valley-minus eigenvectors show large alignment errors and small singular
values relative to the `tr_sewn` target. The table values are checked by
`scripts/verify_manuscript_tables.py`.

### `tab:prb_audit`

Manuscript content:
historical PRB benchmark reconstruction table.

Primary source CSV:
`data/processed/prb_table_reconstruction_nk14.csv`

Historical target source:
`data/processed/prb_manuscript_targets.csv`

Flat-band endpoint source:
`data/processed/flatband_endpoint_audit_nk14.csv`

Reproduction commands:

```bash
python3 scripts/reconstruct_prb_table.py \
  --nk 14 \
  --n-keep-values 2 4 6 \
  --output data/processed/prb_table_reconstruction_nk14.csv

python3 scripts/audit_flatband_endpoint.py \
  --theta-values 1.05 \
  --n-shell-values 3 \
  --mesh-variants half_shift_centered gamma_centered positive_half_shift \
  --band-selectors central_pair closest_abs valence_conduction \
  --output data/processed/flatband_endpoint_audit_nk14.csv
```

Rows mapped into LaTeX:

```text
current tau_z/tau_0, n_keep=2:
  prb_table_reconstruction_nk14.csv
  mode = current_tauz_tau0
  n_keep = 2

double-conv all-tau_z, n_keep=2:
  prb_table_reconstruction_nk14.csv
  mode = double_conv_all_tauz
  n_keep = 2

flat endpoint audit, n_keep=2:
  flatband_endpoint_audit_nk14.csv
  candidate = double_conv_full_curv_all_tauz
  mesh_variant = gamma_centered
  band_selector = central_pair
  theta_deg = 1.05
  n_shell = 3

double-conv all-tau_z, n_keep=6:
  prb_table_reconstruction_nk14.csv
  mode = double_conv_all_tauz
  n_keep = 6
```

Current status:
the audit table intentionally mixes the unified reconstruction route and the
special flat-endpoint audit route. It is a historical benchmark table, not a
production convention for the interband-pairing mechanism scans. The rounded
values are checked by `scripts/verify_manuscript_tables.py`.

## Verification Checklist

Before submission, run:

```bash
python3 scripts/verify_manuscript_tables.py

latexmk -pdf -interaction=nonstopmode -halt-on-error \
  Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex

rg -n 'undefined|Citation|invalid|Overfull|LaTeX Warning|Package hyperref Warning|natbib Warning' \
  Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.log
```

The second command should return no manuscript-level warning lines.

## Remaining Provenance Gap

The current manifest maps every table to a source CSV, and
`scripts/verify_manuscript_tables.py` checks the manuscript values against
those CSV files. The next reproducibility improvement would be full LaTeX table
generation from CSV, but the immediate manual-copy risk is now covered by an
automated verifier.
