# PRB Readiness Audit

Date: 2026-06-09

Manuscript:
`Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex`

## Current Status

The manuscript is a coherent first PRB-style draft, not a submission-ready final
paper. It has a conservative central claim, reproducible figures, explicit
tables, a declarations section, a formal BibTeX file, a figure/table
provenance manifest, and a standalone Supplemental Material skeleton.

The current draft is suitable as a research checkpoint and internal review
target. It still needs additional convergence, a stronger methods appendix, and
final absolute-unit convention decisions before submission.

## Claim Audit

| Claim | Evidence in repo | Status | Manuscript use |
|---|---|---|---|
| Orbital-defined pairing projection is gauge-covariant in the algebraic gate | `notes/gate1_pairing_result_2026-06-07.md`, `scripts/run_pairing_gate.py` | Supported at gate level | Main text methods/results |
| `M1=taux_sigmax` gives useful projected interband pairing weight | `notes/bm_pairing_projection_result_2026-06-07.md`, `data/processed/bm_pairing_projection_tr_sewn_taux_sigmax_nkeep6.csv` | Supported for working convention | Main text |
| `W_inter ~= 0.108` at `eta=1`, `nk=7`, `n_keep=6` | `notes/eta_response_scan_result_2026-06-07.md`, dense scan data | Supported | Main text |
| Fixed-Frobenius response changes by `+0.56%` to `+11.86%` over `mu=-5...5 meV` | `notes/mu_eta_dense_scan_result_2026-06-09.md`, `data/processed/mu_eta_response_scan_nk7_nkeep6_eta1_summary.csv` | Supported at `nk=7` | Main result |
| `nk=9`, `nk=11`, and `nk=13` key points preserve positive fixed-Frobenius response | `data/processed/mu_response_scan_nk9_nkeep6_keypoints_summary.csv`, `data/processed/mu_response_scan_nk11_nkeep6_keypoints_summary.csv`, `data/processed/mu_response_scan_nk13_nkeep6_keypoints_summary.csv`, `notes/nk11_convergence_result_2026-06-09.md`, `notes/nk13_convergence_result_2026-06-09.md` | Supported as selected-grid key-point convergence; not a full continuum extrapolation | Main text plus Supplemental Material |
| Fixed-Delta0 response is weak and can be negative | Dense and key-point scan summaries | Supported | Control result |
| Interband pairing universally enhances physical stiffness | Contradicted by fixed-Delta0 control | Not allowed | Do not claim |
| Absolute PRB benchmark table is reproduced by current production convention | Unit/baseline audits show mismatch | Not allowed | Self-audit only |
| Old `n_keep=6` endpoint can be nearly reconstructed by `double_conv_all_tauz` | `notes/prb_table_reconstruction_result_2026-06-09.md` | Supported as benchmark route | Audit table |
| Old `n_keep=2` endpoint needs mesh/curvature-specific convention | `notes/flatband_endpoint_audit_result_2026-06-09.md` | Supported as historical audit | Appendix/audit |
| Direct comparison to experimental stiffness | Requires final absolute convention and filling calibration | Not ready | Motivation/discussion only |
| Anisotropy is a robust observable signature | Current scans do not establish robustness | Not ready | Secondary diagnostic only |

## Submission-Critical Gaps

1. Convergence:
   The `nk=11` and `nk=13` key-point layers have now been run for
   `mu=-4,0,2,4`, `eta=0,0.5,1`, and `n_keep=6`. They preserve the positive
   fixed-Frobenius response across all selected chemical potentials, and the
   Supplemental Material now includes both a convergence figure and a tabulated
   CSV-verified convergence table. A final submission should still avoid strict
   continuum-limit claims unless a formal extrapolation or denser-mesh
   saturation check is performed.

2. Valley convention:
   The current `tr_sewn` proxy is acceptable for a mechanism diagnostic, but a
   final paper should either implement a fully documented two-valley sewing
   convention or explicitly frame the result as a finite-band diagnostic model.

3. Absolute stiffness:
   The production convention and the historical PRB table are not identical.
   The final paper must choose one absolute convention, recompute all absolute
   values, and keep old-table reconstruction in an appendix or supplemental
   audit.

4. Filling calibration:
   `nu_proxy` is not yet an experimental filling. Any comparison to
   superconducting domes must use calibrated carrier density or be clearly
   qualitative.

5. Reference completeness:
   `references.bib` now covers the cited draft, but the literature matrix still
   marks several rows as needing verification. A final PRB manuscript should
   add a concise comparison paragraph for recent 2025-2026 stiffness and
   pairing-symmetry work.

6. Supplemental reproducibility:
   `notes/figure_table_provenance_2026-06-09.md` now maps every current main
   figure and table to scripts, configs, data files, and reproduction commands.
   `scripts/verify_manuscript_tables.py` checks the main-text and Supplemental
   Material LaTeX table values against the processed CSV files.
   `Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_Supplemental_Material_2026.tex`
   presents the first standalone Supplemental Material skeleton. The remaining
   gap is to expand it with any final convention decisions.

## Recommended Next Work Packages

1. Expand the Supplemental Material:
   add final convergence results, explicit script/config command blocks, and
   any final absolute-convention decision.

2. Decide whether the selected `nk=9/11/13` convergence layer is enough for the
   PRB claim, or whether to add a smaller formal extrapolation plot using one
   or two representative chemical potentials.

3. Add a manuscript appendix section or separate supplement section for the
   PRB benchmark reconstruction, keeping it separate from the main mechanism
   claim.

4. Expand discussion of recent finite-momentum Kekule / PDW scenarios as a
   future extension rather than a covered case.

## Readiness Judgment

Current level: strong internal checkpoint, not yet submission-ready.

The central normalized-response mechanism claim is viable. The final PRB paper
should not be submitted until convergence, valley convention language, and
figure/table provenance are tightened.
