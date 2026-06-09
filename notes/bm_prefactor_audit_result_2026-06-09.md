# BM Baseline and Prefactor Residual Audit

日期：2026-06-09

## Question

Is the PRB baseline mismatch caused by BM bandwidth differences, BZ integration
weights, or a simple missing Kubo prefactor?

## Commands

```text
python3 scripts/audit_bm_baseline.py --theta-values 0.90 0.95 1.00 1.05 1.10 1.15 1.20 --n-shell-values 3 --nk-bandwidth 17 --output data/processed/bm_baseline_theta_scan_nk17.csv

python3 scripts/audit_bm_baseline.py --theta-values 1.05 1.15 1.20 --n-shell-values 3 --nk-bandwidth 17 --nk-response 14 --n-keep-response 2 --output data/processed/bm_baseline_theta_response_nkeep2_nk14.csv

python3 scripts/analyze_prefactor_residuals.py --output data/processed/prefactor_residual_audit_nk14.csv
```

## BM Geometry Check

The reciprocal-lattice geometry is internally consistent:

```text
|b1| = |b2| = 0.0540474 A^-1
BZ area = 0.00252976 A^-2
(2pi)^2 / A_M = 0.00252976 A^-2
```

So the moire-cell and BZ-area factors are not the source of the mismatch.

## Bandwidth Scan

With the current BM implementation:

```text
theta = 1.05 deg -> W2 = 6.096 meV
theta = 1.15 deg -> W2 = 9.401 meV
theta = 1.20 deg -> W2 = 11.758 meV
```

The old PRB text states `W = 11.2 meV` at `theta = 1.05 deg`, so the current
BM baseline does not reproduce that manuscript statement.

However, matching the bandwidth by moving to `theta = 1.20 deg` does not fix
the stiffness baseline:

```text
theta = 1.05 deg -> D_iso = 29.34 eV A^2
theta = 1.20 deg -> D_iso = 31.15 eV A^2
PRB n_keep=2 benchmark -> 67.50 eV A^2
```

Therefore, bandwidth mismatch is a real model-audit issue, but it is not a
sufficient explanation for the stiffness mismatch.

## Prefactor Residuals

Simple global prefactors fail:

```text
current convention, n_keep=2 total scale needed = 2.300
current convention, n_keep=6 total scale needed = 1.510

all_tauz convention, n_keep=2 total scale needed = 2.018
all_tauz convention, n_keep=6 total scale needed = 1.281
```

The sector-level residuals are more informative:

```text
all_tauz, n_keep=2:
conv scale needed = 2.530
geom scale needed = 1.160

all_tauz, n_keep=6:
conv scale needed = 2.099
geom scale needed = 1.001
```

In other words, the `all_tauz` geometric sector already matches the PRB
`n_keep=6` geometric contribution almost exactly, while the conventional sector
remains too small by a factor of roughly two.

## Decision

The next audit should focus on the conventional/intraband sector:

1. whether the PRB table used a diamagnetic or band-curvature conventional term
   in addition to the current-current expression;
2. whether the response convention double-counted Nambu, spin, or paired
   `k/-k` states in the conventional channel only;
3. whether the old table came from a different implementation than the current
   executable pipeline.

For the interband-pairing project, keep using normalized eta-response maps
until the absolute conventional baseline is reconciled.

## Conventional-Channel Follow-Up

See:

```text
notes/conventional_channel_audit_result_2026-06-09.md
```

Summary:

```text
2 * intraband paramagnetic nearly reproduces the PRB conventional value at
n_keep=6, but remains too small at n_keep=2.

Adding a half-curvature term brings n_keep=2 close to the PRB value, but
overshoots n_keep=6.
```

So the conventional-channel mismatch is not resolved by one simple
factor-of-two or curvature correction.
