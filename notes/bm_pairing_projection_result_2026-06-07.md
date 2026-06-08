# BM Pairing Projection Gate Result

日期：2026-06-07

## Question

Does the route-A orbital-defined pairing family tune band-off-diagonal pairing weight after projection using BM eigenvectors?

## Scripts

Main script:

```text
scripts/run_bm_pairing_projection_gate.py
```

Key command:

```text
python3 scripts/run_bm_pairing_projection_gate.py --n-shell 3 --nk 3 --n-keep 6 --partner conjugate_k --m1 taux_sigmax
```

## BM Setup

Current minimal implementation:

```text
theta = 1.05 deg
vF = 2.135 eV Angstrom
w0 = 87.2 meV
w1 = 109.0 meV
n_shell = 3
dimension = 196
```

The code uses the orbital order:

```text
G block -> top_A, top_B, bottom_A, bottom_B
```

## Main Diagnostic

For projected pairing:

```text
Delta_band(k) = U^\dagger(k) Delta_orb U^*(-k)
```

measure:

```text
W_inter = sum_{n != m} |Delta_nm|^2 / sum_{n,m} |Delta_nm|^2
```

## Candidate Screen

Initial candidate:

```text
M1 = taux_sigma0
```

works algebraically, but gives weak two-band off-diagonal weight in the BM projection.

Best current candidate:

```text
M1 = taux_sigmax
```

This candidate gives the largest signal among:

```text
taux_sigma0
tau0_sigmaz
taux_sigmax
tauz_sigmaz
```

## Key Result

Using the time-reversal-aligned proxy:

```text
partner = conjugate_k
M0 = tau0_sigma0
M1 = taux_sigmax
```

the projected off-diagonal weight is controlled by `eta`.

For `n_keep = 2`:

```text
eta = 0.00 -> W_mean = 0.000000
eta = 1.00 -> W_mean = 0.008343
```

For `n_keep = 4`:

```text
eta = 0.00 -> W_mean = 0.000000
eta = 1.00 -> W_mean = 0.070398
```

For `n_keep = 6`:

```text
eta = 0.00 -> W_mean = 0.000000
eta = 1.00 -> W_mean = 0.096977
```

Gauge-projection errors remain at numerical precision, approximately `1e-15`.

## Interpretation

The interband content is much more visible once nearby remote bands are retained. This supports using `n_keep = 4` or `n_keep = 6` as a diagnostic space for pairing structure, while keeping `n_keep = 2` as the flat-band baseline.

The raw `time_reversed_valley` mode produced high off-diagonal weight even for `M0=tau0_sigma0`. That is a warning, not a physics result. It means the valley-plus and valley-minus BM eigenvectors need an explicit sewing convention before `W_inter` can be interpreted as a physical band-basis diagnostic.

## Decision

Proceed with:

```text
M0 = tau0_sigma0
M1 = taux_sigmax
```

Next required implementation:

```text
valley sewing / time-reversal alignment for BM eigenvectors
```

Large stiffness scans should wait until this alignment is documented.
