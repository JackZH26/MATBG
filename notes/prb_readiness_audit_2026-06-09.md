# PRB Readiness Audit

Date: 2026-06-09

Manuscript:
`Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex`

## Current Status

The manuscript is a coherent first PRB-style draft, not a submission-ready final
paper. It has a conservative central claim, reproducible figures, explicit
tables, a declarations section, a formal BibTeX file, a figure/table
provenance manifest, a workflow schematic for the main calculation route, and
a standalone Supplemental Material skeleton.

The current draft is suitable as a research checkpoint and internal review
target. It now has an explicit normalized-response observable policy for the
mechanism-paper scope. It also now has a convergence-sufficiency self-audit
showing that the selected finite-grid evidence is sufficient for the current
normalized mechanism claim, while still not supporting continuum-limit
numerical values. The central-flat-band filling crosswalk now also has a
filling-sufficiency self-audit showing that it is sufficient as a BM counting
reference for the mechanism-paper scope, while still not supporting
device-level carrier-density calibration. A broad 2025-2026 literature sweep
was performed and then refreshed on 2026-06-09; it should still be repeated
immediately before actual submission.
The current draft now includes a central two-flat-band filling crosswalk for
the dense scan, but this is still not a device-specific carrier-density
calibration.

Legacy note: `MATBG_superfluid_weight_PRB_v2.tex` is treated as a historical
baseline source, not as the current submission manuscript. Its author block has
been brought into the current Jian Zhou / JZ Institute format, but its PDF was
not regenerated in this work package because the legacy figure assets
`figures/fig*_v3.pdf` are not present in the current repository.

## Claim Audit

| Claim | Evidence in repo | Status | Manuscript use |
|---|---|---|---|
| Orbital-defined pairing projection is gauge-covariant in the algebraic gate | `notes/gate1_pairing_result_2026-06-07.md`, `scripts/run_pairing_gate.py` | Supported at gate level | Main text methods/results |
| `M1=taux_sigmax` gives useful projected interband pairing weight | `notes/bm_pairing_projection_result_2026-06-07.md`, `data/processed/bm_pairing_projection_tr_sewn_taux_sigmax_nkeep6.csv` | Supported for working convention | Main text |
| `W_inter ~= 0.108` at `eta=1`, `nk=7`, `n_keep=6` | `notes/eta_response_scan_result_2026-06-07.md`, dense scan data | Supported | Main text |
| Fixed-Frobenius response changes by `+0.56%` to `+11.86%` over `mu=-5...5 meV` | `notes/mu_eta_dense_scan_result_2026-06-09.md`, `data/processed/mu_eta_response_scan_nk7_nkeep6_eta1_summary.csv` | Supported at `nk=7` | Main result |
| `nk=9`, `nk=11`, and `nk=13` key points preserve positive fixed-Frobenius response | `data/processed/mu_response_scan_nk9_nkeep6_keypoints_summary.csv`, `data/processed/mu_response_scan_nk11_nkeep6_keypoints_summary.csv`, `data/processed/mu_response_scan_nk13_nkeep6_keypoints_summary.csv`, `notes/nk11_convergence_result_2026-06-09.md`, `notes/nk13_convergence_result_2026-06-09.md` | Supported as selected-grid key-point convergence; not a full continuum extrapolation | Main text plus Supplemental Material |
| Simple `1/nk^2` trend audit keeps fixed-Frobenius key-point intercepts positive | `data/processed/nk_trend_audit_nkeep6.csv`, `figures/nk_trend_audit_nkeep6.pdf`, `notes/nk_trend_audit_result_2026-06-09.md` | Supported as finite-grid trend audit; not a formal continuum limit | Main text plus Supplemental Material |
| `nk=15` spot check preserves positive fixed-Frobenius response at representative key points | `data/processed/mu_response_scan_nk15_nkeep6_spotcheck_summary.csv`, `notes/nk15_spotcheck_result_2026-06-09.md` | Supported for `mu=0,2`; not a dense-grid replacement | Main text plus Supplemental Material |
| Finite-grid evidence is sufficient for the selected-grid normalized mechanism claim | `data/processed/convergence_sufficiency_audit.csv`, `notes/convergence_sufficiency_audit_2026-06-09.md`, `scripts/audit_convergence_sufficiency.py` | Supported for current mechanism-paper scope; not a continuum-limit estimate | Main text plus Supplemental Material |
| Fixed-Delta0 response is weak and can be negative | Dense and key-point scan summaries | Supported | Control result |
| Manuscript keeps the conservative mechanism-paper claim scope | `data/processed/claim_scope_audit.csv`, `notes/claim_scope_audit_2026-06-09.md`, `scripts/audit_claim_scope.py` | Supported as text-level guardrail | Main text plus Supplemental Material |
| Interband pairing universally enhances physical stiffness | Contradicted by fixed-Delta0 control | Not allowed | Do not claim |
| Absolute PRB benchmark table is reproduced by current production convention | Unit/baseline audits show mismatch | Not allowed | Self-audit only |
| Old `n_keep=6` endpoint can be nearly reconstructed by `double_conv_all_tauz` | `notes/prb_table_reconstruction_result_2026-06-09.md` | Supported as benchmark route | Audit table |
| Old `n_keep=2` endpoint needs mesh/curvature-specific convention | `notes/flatband_endpoint_audit_result_2026-06-09.md` | Supported as historical audit | Appendix/audit |
| Direct comparison to experimental stiffness | Requires final absolute convention and device-level filling calibration | Outside current mechanism-paper scope | Motivation/discussion only |
| Central-flat-band filling crosswalk is sufficient as a mechanism-paper counting reference | `data/processed/filling_sufficiency_audit.csv`, `notes/filling_sufficiency_audit_2026-06-09.md`, `scripts/audit_filling_sufficiency.py` | Supported for current mechanism-paper scope; not a device calibration | Main text plus Supplemental Material |
| Anisotropy is a robust observable signature | Current scans do not establish robustness | Not ready | Secondary diagnostic only |

## Submission-Critical Gaps

1. Convergence:
   The `nk=11` and `nk=13` key-point layers have now been run for
   `mu=-4,0,2,4`, `eta=0,0.5,1`, and `n_keep=6`. They preserve the positive
   fixed-Frobenius response across all selected chemical potentials. The
   Supplemental Material now includes the direct convergence figure/table, a
   finite-grid `1/nk^2` trend audit whose fixed-Frobenius intercepts are
   positive at the four key points, and a targeted `nk=15` spot check at
   `mu=0,2`. The convergence-sufficiency self-audit passes all nine checks:
   fixed-Frobenius key-point values remain positive from `6.04%` to `10.13%`,
   the largest per-`mu` selected-grid spread is `2.85` percentage points, the
   two trend-coordinate intercept audits remain positive, and the `nk=15`
   spot-check shifts from `nk=13` are at most `1.16` percentage points. This is
   sufficient for the selected-grid normalized mechanism claim. A final
   submission should still avoid strict continuum-limit claims unless a
   complete denser-mesh saturation check or a more formal extrapolation is
   performed.

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
   The manuscript now states a final observable policy for the current
   mechanism-paper scope: raw response values are internal diagnostics,
   normalized ratios are the only claim-bearing response observables, and eV
   A^2 per-flavor values are used only for benchmark provenance and
   self-audit. A future direct experimental-comparison version must choose one
   absolute convention and recompute any absolute values before comparison.

4. Filling calibration:
   `nu_proxy` is now explicitly defined as a retained-band occupancy label, not
   an experimental filling. The Supplemental Material now includes a central
   two-flat-band crosswalk generated from
   `data/processed/filling_crosswalk_nk7_nshell3.csv`, showing that the dense
   chemical-potential window spans approximately `nu_flat=-4` to `+4` in the
   central-pair counting convention. The filling-sufficiency audit passes all
   nine checks: the crosswalk uses the same 11 chemical potentials as the dense
   response table, `nu_proxy` is strictly increasing, `nu_flat` is
   nondecreasing from `-4.000` to `+4.000`, the dense scan brackets the central
   two-flat-band energy window `[-1.051,4.134] meV`, and the sampled grid
   includes counting-reference points near `nu_flat=0` and `+-2`. This is
   sufficient for the current mechanism-paper filling reference. Any
   comparison to superconducting domes must still use calibrated carrier
   density or remain clearly qualitative.

5. Reference completeness:
   The key recent stiffness and band-off-diagonal pairing references have now
   been added: Tanaka et al. 2025, Christos-Sachdev-Scheurer 2023,
   Putzer-Scheurer 2025, Wang-Levin 2026, and Wang-Chen-Boyack-Levin 2026.
   The 2026-06-09 sweep also added Portoles et al. 2025, Banerjee et al. 2025,
   Park et al. 2025, Kim et al. 2026, Gao et al. 2026, Liang et al. 2026,
   Xiao et al. 2026, and the current author's Zhou 2026 band-basis
   decomposition preprint as benchmark provenance. The previous Lamponen
   placeholder was removed because no matching primary source was identified.
   A final PRB manuscript should still receive a repeat literature sweep
   immediately before submission.

6. Supplemental reproducibility:
   `notes/figure_table_provenance_2026-06-09.md` now maps every current main
   figure and table to scripts, configs, data files, and reproduction commands.
   `scripts/verify_manuscript_tables.py` checks the main-text and Supplemental
   Material LaTeX table values against the processed CSV files. The
   `scripts/audit_claim_scope.py` text-level guardrail checks that the current
   manuscript keeps the required conservative boundary statements and avoids a
   short list of forbidden overclaims.
   `Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_Supplemental_Material_2026.tex`
   presents the first standalone Supplemental Material skeleton. The remaining
   reproducibility gap is to repeat the literature sweep immediately
   before submission and decide whether any expanded-scope experimental
   calibration is desired.

## Recommended Next Work Packages

1. Repeat a broad literature sweep immediately before submission, focused on
   new 2026 stiffness, tunneling, and band-off-diagonal or finite-momentum
   pairing papers.

2. If the manuscript scope is expanded to direct experimental stiffness
   comparison, regenerate absolute values from one declared response convention
   with explicit degeneracy, BZ normalization, and diamagnetic or curvature
   terms.

3. If the manuscript scope is expanded to quantitative superconducting-dome
   comparison, add a device-level carrier-density calibration.

4. Optionally add a broader denser-grid saturation check if the target claim is
   expanded beyond selected-grid sign/scale stability, or if reviewer-facing
   precision becomes central.

## Readiness Judgment

Current level: strong internal checkpoint, not yet submission-ready.

The central normalized-response mechanism claim is viable. The final PRB paper
should not make direct absolute-stiffness or superconducting-dome comparison
claims unless absolute-unit and device-level filling calibrations are added.
For the current mechanism-paper scope, the finite-grid evidence is now
sufficient for the selected-grid normalized mechanism claim, and the
central-flat-band crosswalk is sufficient as a BM counting reference. The main
remaining submission-timing task is to repeat the 2026-06-09 literature sweep
against the then-current literature.
The filling status has improved from an uncalibrated proxy alone to a
CSV-verified and self-audited central-flat-band crosswalk, but the conservative
limitation should remain unless a device-level calibration is added.
