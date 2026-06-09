# PRB Manuscript Strategy

Date: 2026-06-09

## Working Title

Interband Pairing Signatures in the Superfluid Response of Magic-Angle
Twisted Bilayer Graphene

## Central Claim

The executable BM-BdG pipeline supports a conservative mechanism claim:

```text
An orbital-projected interband-pairing direction produces a reproducible
normalization-conditioned change in the isotropic superfluid response across
chemical potential.
```

The strongest quantitative result is the normalized response map:

```text
D_iso(mu, eta) / D_iso(mu, eta=0) - 1
```

with both `fixed_frobenius_norm` and `fixed_delta0` retained as controls.

## Final Observable Policy

For the current PRB mechanism-paper scope, the claim-bearing response
observable is the normalized finite-band response ratio. Raw response values
are internal diagnostics, and eV A^2 per-flavor values are benchmark
provenance only. No absolute stiffness value in the present manuscript is used
as a final experimental prediction.

## Claims Allowed in the Main Text

1. The `tr_sewn` orbital-projected pairing construction passes algebraic and
   projection checks.
2. The interband-pairing weight grows smoothly from zero to about `0.108` at
   `eta=1` for the working `M1=taux_sigmax` direction.
3. In `fixed_frobenius_norm`, `eta=1` changes `D_iso` by about `+0.56%` to
   `+11.86%` across `mu=-5...5 meV` at `nk=7`, `n_keep=6`.
4. `nk=9` key-point checks preserve the qualitative signal.
5. `nk=11/13` key-point checks, a finite-grid trend audit, and a representative
   `nk=15` spot check preserve the positive fixed-Frobenius sign and scale.
6. The convergence-sufficiency self-audit passes all current selected-grid
   gates for the normalized mechanism claim.
7. The filling-sufficiency self-audit supports the central-flat-band crosswalk
   as the current mechanism-paper counting reference.
8. In `fixed_delta0`, the response is much weaker and can be negative.
9. The Discussion identifies falsification checks for this interpretation:
   instability of `W_inter`, loss of fixed-Frobenius sign stability on selected
   higher grids, or a fixed-Delta0 response pattern matching the primary map.
10. Therefore, the effect is a normalization-conditioned mechanism signature,
   not an unconditional absolute-stiffness enhancement.

## Claims Not Allowed Yet

1. Do not claim direct quantitative agreement with experimental stiffness.
2. Do not claim the absolute raw response is a final physical stiffness.
3. Do not reuse the old PRB absolute table as a production convention.
4. Do not claim anisotropy is the primary observable signature.
5. Do not claim `nu_proxy` is a calibrated experimental filling.

## Self-Review Result

The old PRB benchmark table is now best treated as a historical audit route.
It can be partially reconstructed:

```text
n_keep=6:
double_conv_all_tauz gives D_total = 126.66 vs 129.30 eV A^2.

n_keep=2:
gamma_centered + central_pair + double_conv_full_curv_all_tauz gives
D_total = 66.18 vs 67.50 eV A^2.
```

But no single convention reconstructs all sectors and truncations cleanly.
Thus new paper figures use normalized mechanism quantities. A direct
experimental-comparison paper would need a separate absolute convention
declared and recomputed end-to-end.

## Proposed Paper Structure

1. Introduction: MATBG stiffness, quantum geometry, and why pairing structure
   matters.
2. Model and pairing construction: BM model, `tr_sewn` pairing, orbital
   matrices, normalization controls.
3. Response decomposition: finite-band BdG response, current split, normalized
   observables.
4. Pairing-definition gates: gauge covariance, interband weight, velocity
   decomposition.
5. Eta and mu response maps: dense scan, heatmaps, `nk=9` validation.
6. Self-review of absolute units: PRB benchmark reconstruction and why
   absolute claims are deferred.
7. Discussion and outlook.

## Primary Figures

1. `figures/workflow_schematic_prb.png`
2. `figures/mu_eta_heatmap_nk7_nkeep6_fixed_frobenius.png`
3. `figures/mu_eta_heatmap_nk7_nkeep6_fixed_delta0.png`

Supporting generated figures currently kept outside the main manuscript:

1. `figures/mu_response_scan_nk7_nkeep6.png`
2. `figures/eta_response_scan_nk7_nkeep6.png`
3. `figures/nk_convergence_keypoints_nkeep6.png`
4. `figures/nk_trend_audit_nkeep6.png`

## Primary Tables

1. Dense `eta=1` response summary.
2. `nk=9` key-point validation.
3. PRB reconstruction audit table.

## Draft File

```text
Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex
```

## Supplemental Material Draft

```text
Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_Supplemental_Material_2026.tex
```

## Cover Letter Draft

```text
submission/Zhou_PRB_Cover_Letter_2026.md
```

## Current Manuscript Infrastructure

1. Bibliography is managed through `references.bib`.
2. Submission-readiness risks are tracked in
   `notes/prb_readiness_audit_2026-06-09.md`.
3. Figure and table provenance is tracked in
   `notes/figure_table_provenance_2026-06-09.md`.
4. Manuscript and Supplemental Material table values are checked against
   processed CSV files by
   `scripts/verify_manuscript_tables.py`.
5. Recent 2025-2026 stiffness, Kekule/PDW, strong-correlation, and
   interaction-reshaped-band context is tracked in
   `notes/recent_literature_update_2026-06-09.md`.
6. The selected `nk=11` and `nk=13` convergence checks are tracked in
   `notes/nk11_convergence_result_2026-06-09.md`,
   `notes/nk13_convergence_result_2026-06-09.md`,
   `configs/mu_response_convergence_nk11.yaml`, and
   `configs/mu_response_convergence_nk13.yaml`.
7. The selected-grid convergence figure is generated by
   `scripts/plot_nk_convergence_keypoints.py`.
8. The main workflow schematic is generated by
   `scripts/plot_workflow_schematic.py`.
9. The selected-grid convergence sufficiency decision is tracked in
   `notes/convergence_sufficiency_audit_2026-06-09.md`,
   `data/processed/convergence_sufficiency_audit.csv`, and
   `scripts/audit_convergence_sufficiency.py`.
10. The central-flat-band filling sufficiency decision is tracked in
   `notes/filling_sufficiency_audit_2026-06-09.md`,
   `data/processed/filling_sufficiency_audit.csv`, and
   `scripts/audit_filling_sufficiency.py`.
11. The `tr_sewn` valley convention is documented in the main text and
   Supplemental Material, with the raw-valley diagnostic tracked by
   `notes/valley_sewing_convention.md`,
   `configs/valley_sewing_diagnostic.yaml`, and
   `data/processed/valley_sewing_diagnostic.csv`.
12. The manuscript reporting convention separates raw diagnostics, normalized
   mechanism ratios, eV A^2 per-flavor benchmark audits, and the retained-band
   filling proxy; details are tracked in
   `notes/normalization_and_units_strategy.md` and
   `notes/observable_policy_decision_2026-06-09.md`.
13. Recent stiffness and band-off-diagonal pairing context is now included in
    the manuscript through `tanaka_2025`, `christos_2023`, `putzer_2025`,
    `wang_kekule_2026`, `liang_gutzwiller_2026`, and
    `xiao_flat_bands_2026`; supporting notes are in
    `notes/recent_literature_update_2026-06-09.md`.
14. Text-level guardrails are run with `scripts/audit_claim_scope.py` and
    `scripts/audit_observable_policy.py`.
15. Submission-package mechanical guardrails are run with
    `scripts/audit_submission_package.py`, which writes
    `data/processed/submission_package_audit.csv` and is summarized in
    `notes/submission_package_audit_2026-06-09.md`.
16. The standard one-command validation chain is
    `scripts/run_prb_validation.py`, which writes
    `data/processed/prb_validation_summary.csv` and is summarized in
    `notes/prb_validation_chain_2026-06-09.md`.
17. The current manuscript package inventory is generated by
    `scripts/build_prb_submission_manifest.py`, which writes
    `data/processed/prb_submission_manifest.csv` and is summarized in
    `notes/prb_submission_manifest_2026-06-09.md`.
18. The current PRB cover letter draft is
    `submission/Zhou_PRB_Cover_Letter_2026.md`; its target journal, title,
    conservative scope statement, originality statement, and required signature
    are checked by `scripts/audit_submission_package.py`.
19. The local PRB checkpoint package is generated by
    `scripts/build_prb_submission_package.py`, which copies journal-facing
    files and provenance material into ignored outputs under
    `submission/build/` and writes
    `data/processed/prb_submission_package_build.csv`.
20. The current Abstract and Introduction foreground the normalized-response
    mechanism question, the fixed-Frobenius/fixed-Delta0 contrast, and the
    selected-grid stability evidence before the absolute-unit and filling
    limitations.
