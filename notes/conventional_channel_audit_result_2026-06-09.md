# Conventional Channel Audit

日期：2026-06-09

## Question

Does the PRB conventional baseline require an additional band-curvature or
diamagnetic-like term beyond the current intraband paramagnetic expression?

## Command

```text
python3 scripts/audit_conventional_channel.py --nk 14 --n-keep-values 2 6 --curvature-dk-values 3e-4 1e-4 3e-5 --output data/processed/conventional_channel_audit_nk14.csv
```

## Result

At `curvature_dk = 1e-4 A^-1`:

```text
n_keep = 2:
paramagnetic_tauz                     = 20.95 eV A^2  (-60.48%)
2 * paramagnetic_tauz                 = 41.89 eV A^2  (-20.96%)
2 * paramagnetic_tauz + 0.5 curvature = 49.94 eV A^2  ( -5.77%)
2 * paramagnetic_tauz + curvature     = 57.99 eV A^2  ( +9.42%)
PRB conventional benchmark            = 53.00 eV A^2

n_keep = 6:
paramagnetic_tauz                     = 25.72 eV A^2  (-52.36%)
2 * paramagnetic_tauz                 = 51.45 eV A^2  ( -4.73%)
2 * paramagnetic_tauz + 0.5 curvature = 60.92 eV A^2  (+12.82%)
2 * paramagnetic_tauz + curvature     = 70.40 eV A^2  (+30.37%)
PRB conventional benchmark            = 54.00 eV A^2
```

The curvature finite-difference estimate is stable across
`dk = 3e-4, 1e-4, 3e-5 A^-1` at the few-percent level for `n_keep=6` and
sub-percent level for `n_keep=2`.

## Interpretation

A factor of two multiplying the intraband paramagnetic expression nearly
reproduces the PRB conventional value at `n_keep=6`, but remains too small at
`n_keep=2`.

Adding a half-curvature term brings `n_keep=2` close to the PRB benchmark, but
then overshoots `n_keep=6`. Therefore the PRB conventional baseline is not
reproduced by a single simple formula among the audited candidates.

The likely remaining possibilities are:

1. the old PRB table used a different BM band structure or velocity convention;
2. the old conventional channel included a factor-of-two counting convention,
   plus an additional low-band correction;
3. the current and old implementations partitioned conventional/geometric
   weight differently even if the total response was intended to match.

## Decision

Do not change the production response convention yet. The next step should be
to reconstruct the PRB table from first principles in a dedicated benchmark
script, keeping the current interband-pairing scans normalized and separate.
