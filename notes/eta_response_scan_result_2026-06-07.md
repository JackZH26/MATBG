# Dense Eta Response Scan Result

日期：2026-06-07

## Question

After caching the k-resolved BM data, does the response vary smoothly with interband-mixing parameter `eta`?

## Command

```text
python3 scripts/run_eta_response_scan.py --n-shell 3 --nk 7 --n-keep 6 --output data/processed/eta_response_scan_nk7_nkeep6.csv
python3 scripts/plot_eta_response_scan.py --input data/processed/eta_response_scan_nk7_nkeep6.csv --output figures/eta_response_scan_nk7_nkeep6.png --summary data/processed/eta_response_scan_nk7_nkeep6_summary.csv
```

## Files

```text
data/processed/eta_response_scan_nk7_nkeep6.csv
data/processed/eta_response_scan_nk7_nkeep6_summary.csv
figures/eta_response_scan_nk7_nkeep6.png
figures/eta_response_scan_nk7_nkeep6.pdf
```

## Setup

```text
n_shell = 3
nk = 7
n_keep = 6
mu = 0 meV
Delta0 = 1 meV
partner = tr_sewn
M0 = tau0_sigma0
M1 = taux_sigmax
eta = 0.0 ... 1.0 in steps of 0.1
```

## Summary

The projected interband pairing weight increases smoothly:

```text
W_pair: 0.0000 -> 0.1082
```

The isotropic total response,

```text
D_iso = (Dxx_total + Dyy_total) / 2
```

changes by:

```text
fixed_frobenius_norm: +8.17%
fixed_delta0:         +1.12%
```

The geometric fraction changes by:

```text
fixed_frobenius_norm: 0.7079 -> 0.7264
fixed_delta0:         0.7081 -> 0.7041
```

The anisotropy ratio stays close to one:

```text
fixed_frobenius_norm: 0.9774 to 1.0184
fixed_delta0:         1.0050 to 1.0184
```

## Interpretation

This scan supports a narrow but useful working result:

```text
Increasing eta creates controlled projected interband pairing weight and produces a smooth raw BdG response change.
```

The normalization comparison matters. Fixed-Frobenius normalization gives a visible `D_iso` enhancement, while fixed raw `Delta0` gives only a small enhancement. Therefore any later claim must distinguish:

1. pairing-structure effect at fixed projected/orbital norm;
2. response at fixed raw gap amplitude.

At this grid, anisotropy is not a strong signature. It is small and remains close to one.

## Decision

Next step:

```text
Run a chemical-potential scan at eta = 0, 0.5, 1.0 for both normalization modes.
```

The first mu scan should use:

```text
nk = 7
n_keep = 6
mu = -6, -4, -2, 0, 2, 4, 6 meV
```

This is enough to test whether the eta-driven response differs across filling before investing in a denser map.
