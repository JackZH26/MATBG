# Minimal BdG Response Gate Result

日期：2026-06-07

## Question

Can the current BM + pairing infrastructure produce finite `Dtotal/Dconv/Dgeom/Dcross` response components with clean numerical closure?

## Conventions

Pairing:

```text
partner = tr_sewn
M0 = tau0_sigma0
M1 = taux_sigmax
Delta_orb(eta) = Delta0 normalize[M0 + eta M1]
```

Current split:

```text
band-diagonal velocity     -> tau_z Nambu current -> Dconv
band-off-diagonal velocity -> tau_0 Nambu current -> Dgeom
Dcross = Dtotal - Dconv - Dgeom
```

This matches the working manuscript convention for the band-basis decomposition.

## Important Limitations

The output is a gate-level raw response:

1. no moire-cell area factor;
2. no spin/valley degeneracy factor;
3. no diamagnetic counterterm;
4. no comparison to the existing PRB table yet;
5. current convention still needs final methods-level derivation before manuscript use.

Therefore the present numbers should be read as mechanism diagnostics, not final physical stiffness values.

## Commands

```text
python3 scripts/run_bdg_response_gate.py --n-shell 3 --nk 3 --n-keep 2 --etas 0 0.5 1.0 --output data/processed/bdg_response_gate_nkeep2.csv
python3 scripts/run_bdg_response_gate.py --n-shell 3 --nk 3 --n-keep 4 --etas 0 0.5 1.0 --output data/processed/bdg_response_gate_nkeep4.csv
python3 scripts/run_bdg_response_gate.py --n-shell 3 --nk 3 --n-keep 6 --etas 0 0.5 1.0 --output data/processed/bdg_response_gate_nkeep6.csv
python3 scripts/run_bdg_response_gate.py --n-shell 3 --nk 5 --n-keep 4 --etas 0 0.5 1.0 --output data/processed/bdg_response_gate_nk5_nkeep4.csv
python3 scripts/run_bdg_response_gate.py --n-shell 3 --nk 5 --n-keep 4 --normalization fixed_delta0 --etas 0 0.5 1.0 --output data/processed/bdg_response_gate_nk5_nkeep4_fixed_delta0.csv
```

## Numerical Checks

All runs pass:

```text
BdG Hermiticity error: ~1e-15
particle-hole spectrum error: ~1e-15
decomposition closure error: 0 within recorded precision
```

## First Trend

For the `nk=5`, `n_keep=4`, fixed-Frobenius-norm check:

```text
eta = 0.0 -> W_pair = 0.0000, Dxx_total = 59717.104, Dyy_total = 63724.696
eta = 0.5 -> W_pair = 0.0168, Dxx_total = 62948.173, Dyy_total = 65155.420
eta = 1.0 -> W_pair = 0.0636, Dxx_total = 71139.984, Dyy_total = 68834.130
```

For the same grid with fixed raw `Delta0`:

```text
eta = 0.0 -> W_pair = 0.0000, Dxx_total = 59717.104, Dyy_total = 63724.696
eta = 0.5 -> W_pair = 0.0168, Dxx_total = 59889.758, Dyy_total = 63018.709
eta = 1.0 -> W_pair = 0.0636, Dxx_total = 60931.654, Dyy_total = 62403.836
```

The effect survives the normalization change but is much weaker in the fixed-`Delta0` scan. This is useful: it separates pairing-structure response from raw gap-norm effects.

## Interpretation

The first response gate shows that the pipeline can now generate:

```text
Dtotal
Dconv
Dgeom
Dcross
Dxx/Dyy anisotropy
pairing off-diagonal diagnostic W_pair
```

The strongest trend at this stage is not a final anisotropy claim. The `nk=3` runs show large artificial anisotropy, while `nk=5` is much closer to isotropic at `eta=0`. Mesh convergence must therefore precede any claim about `Dxx/Dyy`.

The robust near-term claim is narrower:

```text
With tr_sewn pairing and M1=taux_sigmax, increasing eta produces a finite interband pairing diagnostic and changes the raw finite-band BdG stiffness response with clean numerical closure.
```

## Decision

Proceed to a small convergence grid:

```text
nk = 5, 7
n_keep = 2, 4, 6
eta = 0, 0.25, 0.5, 0.75, 1
normalization = fixed_frobenius_norm and fixed_delta0
```

Only after that should the project begin interpreting observable signatures.

## Convergence Snapshot

The first small convergence grid used:

```text
nk = 5, 7
n_keep = 2, 4, 6
eta = 0, 0.5, 1.0
normalization = fixed_frobenius_norm
```

Key observations:

1. The total response generally increases with `eta`.
2. The anisotropy ratio is still mesh and `n_keep` sensitive.
3. The `n_keep=6` results are much closer to isotropic than the very coarse `nk=3` checks.
4. The cross term is nonzero once `eta` is nonzero, but remains smaller than the conv/geom pieces in the current gate runs.

Representative `nk=7`, `n_keep=6`, fixed-Frobenius result:

```text
eta = 0.0 -> W_pair = 0.0000, Dxx_total = 85042.816, Dyy_total = 83503.049
eta = 0.5 -> W_pair = 0.0304, Dxx_total = 87217.330, Dyy_total = 86525.435
eta = 1.0 -> W_pair = 0.1082, Dxx_total = 90117.668, Dyy_total = 92197.891
```

Fixed raw `Delta0` at the same `nk=7`, `n_keep=6` gives a weaker response:

```text
eta = 0.0 -> W_pair = 0.0000, Dxx_total = 85042.816, Dyy_total = 83503.049
eta = 0.5 -> W_pair = 0.0304, Dxx_total = 85284.096, Dyy_total = 84066.344
eta = 1.0 -> W_pair = 0.1082, Dxx_total = 85425.880, Dyy_total = 85004.017
```

This reinforces the need to carry both normalization modes. A stiffness change that appears only in fixed-Frobenius mode should be described carefully as a projected-gap-structure effect, not as a simple interband-pairing signature.

Updated next step:

```text
1. Refactor response code so the same k-resolved data can be reused across eta scans.
2. Add a dense eta grid at nk=7 for n_keep=6.
3. Add mu scan only after the eta trend is stable.
```
