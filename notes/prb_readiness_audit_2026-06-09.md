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
target. It still needs a final absolute-unit convention, filling calibration,
and a final pre-submission literature sweep before submission.
The current draft now includes a central two-flat-band filling crosswalk for
the dense scan, but this is still not a device-specific carrier-density
calibration.

## Claim Audit

| Claim | Evidence in repo | Status | Manuscript use |
|---|---|---|---|
| Orbital-defined pairing projection is gauge-covariant in the algebraic gate | `notes/gate1_pairing_result_2026-06-07.md`, `scripts/run_pairing_gate.py` | Supported at gate level | Main text methods/results |
| `M1=taux_sigmax` gives useful projected interband pairing weight | `notes/bm_pairing_projection_result_2026-06-07.md`, `data/processed/bm_pairing_projection_tr_sewn_taux_sigmax_nkeep6.csv` | Supported for working convention | Main text |
| `W_inter ~= 0.108` at `eta=1`, `nk=7`, `n_keep=6` | `notes/eta_response_scan_result_2026-06-07.md`, dense scan data | Supported | Main text |
| Fixed-Frobenius response changes by `+0.56%` to `+11.86%` over `mu=-5...5 meV` | `notes/mu_eta_dense_scan_result_2026-06-09.md`, `data/processed/mu_eta_response_scan_nk7_nkeep6_eta1_summary.csv` | Supported at `nk=7` | Main result |
| `nk=9`, `nk=11`, and `nk=13` key points preserve positive fixed-Frobenius response | `data/processed/mu_response_scan_nk9_nkeep6_keypoints_summary.csv`, `data/processed/mu_response_scan_nk11_nkeep6_keypoints_summary.csv`, `data/processed/mu_response_scan_nk13_nkeep6_keypoints_summary.csv`, `notes/nk11_convergence_result_2026-06-09.md`, `notes/nk13_convergence_result_2026-06-09.md` | Supported as selected-grid key-point convergence; not a full continuum extrapolation | Main text plus Supplemental Material |
| Simple `1/nk^2` trend audit keeps fixed-Frobenius key-point intercepts positive | `data/processed/nk_trend_audit_nkeep6.csv`, `figures/nk_trend_audit_nkeep6.pdf`, `notes/nk_trend_audit_result_2026-06-09.md` | Supported as finite-grid trend audit; not a formal continuum limit | Main text plus Supplemental Material |
| Fixed-Delta0 response is weak and can be negative | Dense and key-point scan summaries | Supported | Control result |
| Interband pairing universally enhances physical stiffness | Contradicted by fixed-Delta0 control | Not allowed | Do not claim |
| Absolute PRB benchmark table is reproduced by current production convention | Unit/baseline audits show mismatch | Not allowed | Self-audit only |
| Old `n_keep=6` endpoint can be nearly reconstructed by `double_conv_all_tauz` | `notes/prb_table_reconstruction_result_2026-06-09.md` | Supported as benchmark route | Audit table |
| Old `n_keep=2` endpoint needs mesh/curvature-specific convention | `notes/flatband_endpoint_audit_result_2026-06-09.md` | Supported as historical audit | Appendix/audit |
| Direct comparison to experimental stiffness | Requires final absolute convention and device-level filling calibration | Not ready | Motivation/discussion only |
| Anisotropy is a robust observable signature | Current scans do not establish robustness | Not ready | Secondary diagnostic only |

## Submission-Critical Gaps

1. Convergence:
   The `nk=11` and `nk=13` key-point layers have now been run for
   `mu=-4,0,2,4`, `eta=0,0.5,1`, and `n_keep=6`. They preserve the positive
   fixed-Frobenius response across all selected chemical potentials. The
   Supplemental Material now includes both the direct convergence figure/table
   and a finite-grid `1/nk^2` trend audit whose fixed-Frobenius intercepts are
   positive at the four key points. A final submission should still avoid
   strict continuum-limit claims unless a denser-mesh saturation check or a
   more formal extrapolation is performed.

2. Valley convention:
   The current `tr_sewn` proxy is now explicitly documented in the main text
   and Supplemental Material. The Supplemental Material includes a raw-valley
   diagnostic table showing that independently diagonalized valley-minus
   eigenvectors are not in the target time-reversal sewing convention. This
   supports the finite-band diagnostic framing. A fully independent two-valley
   implementation remains necessary before studying valley-asymmetric
   perturbations, strain, or explicitly valley-dependent interactions.

3. Absolute stiffness:
   The production convention and the historical PRB table are not identical.
   The manuscript now states a three-layer reporting convention: raw response
   values are internal diagnostics, normalized ratios are the main mechanism
   observable, and eV A^2 per-flavor values are used only for the benchmark
   self-audit. The final paper must still choose one absolute convention and
   recompute any absolute values before direct experimental comparison.

4. Filling calibration:
   `nu_proxy` is now explicitly defined as a retained-band occupancy label, not
   an experimental filling. The Supplemental Material now includes a central
   two-flat-band crosswalk generated from
   `data/processed/filling_crosswalk_nk7_nshell3.csv`, showing that the dense
   chemical-potential window spans approximately `nu_flat=-4` to `+4` in the
   central-pair counting convention. Any comparison to superconducting domes
   must still use calibrated carrier density or remain clearly qualitative.

5. Reference completeness:
   The key recent stiffness and band-off-diagonal pairing references have now
   been added: Tanaka et al. 2025, Christos-Sachdev-Scheurer 2023,
   Putzer-Scheurer 2025, and Wang-Chen-Boyack-Levin 2026. The previous
   Lamponen placeholder was removed because no matching primary source was
   identified. A final PRB manuscript should still receive a broad
   pre-submission literature sweep.

6. Supplemental reproducibility:
   `notes/figure_table_provenance_2026-06-09.md` now maps every current main
   figure and table to scripts, configs, data files, and reproduction commands.
   `scripts/verify_manuscript_tables.py` checks the main-text and Supplemental
   Material LaTeX table values against the processed CSV files.
   `Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_Supplemental_Material_2026.tex`
   presents the first standalone Supplemental Material skeleton. The remaining
   gap is to expand it with any final convention decisions.

## Recommended Next Work Packages

1. Decide the final absolute stiffness convention:
   if absolute values are needed, regenerate them from one declared response
   convention with explicit degeneracy, BZ normalization, and diamagnetic or
   curvature terms.

2. Decide whether the selected `nk=9/11/13` trend audit is enough for the PRB
   mechanism claim, or whether to add a denser-grid saturation check using one
   or two representative chemical potentials.

3. Decide whether the central-flat-band crosswalk is sufficient for the PRB
   mechanism claim, or add a device-level carrier-density calibration before
   comparing to superconducting dome locations.

4. Perform a final broad literature sweep before submission, focused on new
   2026 stiffness, tunneling, and band-off-diagonal pairing papers.

## Readiness Judgment

Current level: strong internal checkpoint, not yet submission-ready.

The central normalized-response mechanism claim is viable. The final PRB paper
should not be submitted until the remaining absolute-unit convention, filling
calibration, and final literature sweep are tightened.
The filling status has improved from an uncalibrated proxy alone to a
CSV-verified central-flat-band crosswalk, but the conservative limitation should
remain unless a device-level calibration is added.
