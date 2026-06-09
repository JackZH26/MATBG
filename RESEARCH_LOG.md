# Research Log

## 2026-06-07

Question: How should the proposal be turned into an executable research plan?

Config / run_id: planning only.

Result: Created `MATBG_Executable_Research_Plan_2026.md` and initialized Sprint 1 artifacts.

Decision: Treat interband pairing definition as Gate 1. Do not begin large scans until the gauge-covariant pairing construction is fixed and tested.

Question: Can the first orbital-projected interband pairing family pass the algebraic Gate 1 checks?

Config / run_id: `python3 scripts/run_pairing_definition_gate.py`

Result: All toy algebra checks passed. With `M0 = tau0_sigma0` and `M1 = taux_sigma0`, the time-reversal-like toy setup gives `W_inter = 0` at `eta = 0` and increases to about `0.298` at `eta = 1.0`; gauge projection and spectrum errors are at numerical precision.

Decision: Use route A, orbital-defined projected pairing, as the first implementation route. Next step is to connect the same pairing functions to BM eigenvectors rather than random toy bases.

Question: Does the route-A pairing family tune off-diagonal pairing weight after projection with BM eigenvectors?

Config / run_id: `python3 scripts/run_bm_pairing_projection_gate.py --n-shell 3 --nk 3 --partner conjugate_k --m1 taux_sigmax`

Result: The initial `taux_sigma0` candidate is weak in the two-band projection. Screening candidate matrices shows `taux_sigmax` is stronger. In the time-reversal-aligned proxy, `M0=tau0_sigma0` gives zero off-diagonal weight and `M1=taux_sigmax` increases `W_inter` with `eta`; for `n_keep=6`, the fixed-norm mean rises from `0` to about `0.097` at `eta=1`.

Decision: Use `M1=taux_sigmax` as the current BM-projection candidate. Before stiffness scans, implement or document the valley-basis sewing convention because raw valley-plus / valley-minus eigenvectors make even `M0` appear highly off-diagonal.

Question: Which valley sewing convention should be used for the pairing projection gate?

Config / run_id: `python3 scripts/run_valley_sewing_diagnostic.py --n-shell 3 --nk 3 --n-keep-values 2 4 6`

Result: Raw valley-minus eigenvectors are not aligned with the identity-orbital time-reversal target. Minimum singular values are very small: about `0.022` for `n_keep=2`, `0.004` for `n_keep=4`, and `0.002` for `n_keep=6`.

Decision: Use `partner=tr_sewn`, defined by `U_-(-k)=U_+(k)^*`, as the working valley sewing convention for the next stage. Keep raw valley-minus modes only as diagnostics.

Question: Does the BM velocity projection support a clean intra/inter current split?

Config / run_id: `python3 scripts/run_bm_velocity_projection_gate.py --n-shell 3 --nk 3 --n-keep-values 2 4 6`

Result: Projected velocity matrices are Hermitian to `~1e-15`, and the diagonal/off-diagonal decomposition closes exactly. Off-diagonal velocity weight is substantial: roughly `0.46-0.55` for `n_keep=2`, `0.75-0.78` for `n_keep=4`, and `0.75-0.84` for `n_keep=6`.

Decision: The normal-state velocity projection scaffold is ready. Next step is a minimal BdG response engine using the fixed `tr_sewn` pairing convention and the diagonal/off-diagonal velocity split.

Question: Can the first finite-band BdG response engine produce stiffness components with clean closure?

Config / run_id: `scripts/run_bdg_response_gate.py` with `tr_sewn`, `M0=tau0_sigma0`, `M1=taux_sigmax`, `nk=3/5`, `n_keep=2/4/6`.

Result: The first response gate runs successfully. BdG Hermiticity and particle-hole spectrum errors are `~1e-15`, and `Dtotal = Dconv + Dgeom + Dcross` closes by construction. For `nk=5`, `n_keep=4`, fixed-Frobenius norm, `eta=0 -> 1` changes `Dxx_total` from `59717` to `71140` and `Dyy_total` from `63725` to `68834` in raw response units.

Decision: Treat these as mechanism diagnostics only. The next task is a small convergence grid before making any observable-signature claim.

Question: Does the first response trend survive a small `nk` and `n_keep` convergence check?

Config / run_id: `nk=5,7`, `n_keep=2,4,6`, `eta=0,0.5,1.0`, plus `nk=7,n_keep=6,fixed_delta0`.

Result: Total response generally increases with `eta`, but anisotropy is not yet robust. For `nk=7,n_keep=6`, fixed-Frobenius gives `Dxx_total: 85043 -> 90118` and `Dyy_total: 83503 -> 92198` from `eta=0 -> 1`. Fixed raw `Delta0` gives a much weaker change, `Dxx_total: 85043 -> 85426` and `Dyy_total: 83503 -> 85004`.

Decision: Carry both normalization modes. Do not claim anisotropy yet. Next step is a denser eta grid and then a mu scan only after the eta trend is stable.

Question: Does a dense eta grid show a smooth response trend?

Config / run_id: `python3 scripts/run_eta_response_scan.py --n-shell 3 --nk 7 --n-keep 6`, followed by `scripts/plot_eta_response_scan.py`.

Result: Dense eta scan is smooth. `W_pair` increases from `0` to `0.1082`. Isotropic total response increases by `8.17%` in fixed-Frobenius mode and `1.12%` in fixed-Delta0 mode. Geometric fraction rises from `0.7079` to `0.7264` in fixed-Frobenius mode but slightly decreases in fixed-Delta0 mode. Anisotropy remains close to one.

Decision: Eta trend is stable enough to start the first mu scan. Use `eta = 0, 0.5, 1.0`, `mu = -6,-4,-2,0,2,4,6 meV`, both normalization modes.

Question: Does the eta-dependent response persist across chemical potential?

Config / run_id: `python3 scripts/run_mu_response_scan.py --n-shell 3 --nk 7 --n-keep 6`.

Result: Fixed-Frobenius mode shows an eta=1 relative D_iso increase between about `5.4%` and `11.5%` across `mu=-6...6 meV`. Fixed-Delta0 mode is much weaker, between about `-1.1%` and `+3.6%`. The geometric fraction follows a doping-dependent trend and remains useful as an explanation variable.

Decision: Doping dependence is promising enough for a denser mu scan, but the main text must not claim unconditional stiffness enhancement. The normalization convention is now a first-class control parameter.

## 2026-06-09

Question: Does a denser mu-eta response map preserve the eta-dependent signature?

Config / run_id: `mu=-5...5 meV`, `eta=0,0.25,0.5,0.75,1`, `nk=7`, `n_keep=6`; plus `nk=9` key-point check at `mu=-4,0,2,4`.

Result: Fixed-Frobenius mode gives eta=1 relative D_iso changes from about `+0.56%` to `+11.86%` across the dense mu grid. The `nk=9` key-point check gives `+6.04%`, `+8.63%`, `+6.43%`, and `+6.05%` at `mu=-4,0,2,4`. Fixed-Delta0 remains weak and can be slightly negative.

Decision: The eta response is reproducible as a normalization-conditioned mechanism signature. Next work should focus on unit conversion/baseline matching and deciding the main normalization convention.

Question: Does the current response engine reproduce the PRB uniform-s baseline after unit conversion?

Config / run_id: `scripts/convert_response_units.py`, `scripts/run_band_diagonal_response_gate.py --nk 14 --n-keep-values 2 4 6`, and `scripts/compare_prb_baseline.py`.

Result: The moire constants match the manuscript convention: `A_M = 15605.57 A^2` and `G_M = 0.054047 A^-1`. Raw response values convert conservatively as `raw meV A^2 / 1000 = eV A^2` per flavor. However, the explicit band-diagonal uniform-s route at `nk=14` gives `D_iso = 29.34 eV A^2` for `n_keep=2` and `85.60 eV A^2` for `n_keep=6`, below the PRB benchmark values `67.5` and `129.3 eV A^2`.

Decision: The baseline mismatch is not caused mainly by the new orbital-projected pairing ansatz and is not a single global unit factor. Before manuscript-level absolute tables, audit Kubo prefactors, Nambu current convention, BZ integration weights, and the previous PRB implementation. Continue using normalized eta-response quantities for mechanism figures.

Question: Is the PRB baseline mismatch mostly due to the Nambu current convention?

Config / run_id: `python3 scripts/audit_response_conventions.py --nk 14 --n-keep-values 2 6`.

Result: Switching from the current `intra_tauz_inter_tau0` convention to `all_tauz` moves the band-diagonal baseline closer to the PRB table, but does not close the gap. For `n_keep=2`, `D_iso` changes from `29.34` to `33.45 eV A^2` versus PRB `67.5`; for `n_keep=6`, it changes from `85.60` to `100.94 eV A^2` versus PRB `129.3`.

Decision: Current convention is a contributor but not the whole discrepancy. Continue the audit by checking Kubo prefactors, BZ integration weights, and any older-code implementation differences before changing the production response convention.
