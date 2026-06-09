# Unit Conversion and PRB Baseline Check

日期：2026-06-09

## Question

Can the current finite-band response outputs be converted into the PRB
manuscript convention, and does the `eta=0` baseline reproduce the previous
uniform-s benchmark?

## Commands

```text
python3 scripts/convert_response_units.py data/processed/mu_eta_response_scan_nk7_nkeep6.csv --output data/processed/mu_eta_response_scan_nk7_nkeep6_units.csv

python3 scripts/run_bdg_response_gate.py --nk 14 --n-keep 2 --etas 0 --output data/processed/bdg_response_gate_nk14_nkeep2_eta0_units_check.csv

python3 scripts/run_bdg_response_gate.py --nk 14 --n-keep 6 --etas 0 --output data/processed/bdg_response_gate_nk14_nkeep6_eta0_units_check.csv

python3 scripts/run_band_diagonal_response_gate.py --nk 14 --n-keep-values 2 4 6 --output data/processed/band_diagonal_response_baseline_nk14.csv

python3 scripts/compare_prb_baseline.py data/processed/band_diagonal_response_baseline_nk14.csv --normalization band_delta0 --output data/processed/prb_baseline_compare_band_diagonal_nk14.csv
```

## Unit Constants

The new unit helper gives:

```text
theta = 1.05 deg
moire_cell_area_A2 = 15605.5711
moire_reciprocal_scale_Ainv = 0.0540474
```

This agrees with the manuscript convention:

```text
A_M = 15606 A^2
G_M = 0.054 A^-1
```

The conservative response conversion is:

```text
raw meV A^2 / 1000 = eV A^2 per flavor
```

The spin/valley factor is reported as a separate optional factor of 4, not
folded into the per-flavor benchmark comparison.

## Baseline Comparison

For the explicit band-diagonal uniform-s route at `nk=14`:

```text
n_keep = 2:
current D_iso = 29.34 eV A^2
PRB benchmark = 67.50 eV A^2
relative delta = -56.53%
current geometric fraction = 28.6%
PRB geometric fraction = 21.5%

n_keep = 6:
current D_iso = 85.60 eV A^2
PRB benchmark = 129.30 eV A^2
relative delta = -33.79%
current geometric fraction = 70.0%
PRB geometric fraction = 58.3%
```

The orbital-projected `eta=0` baseline gives essentially the same result as
the explicit band-diagonal route, so the mismatch is not mainly caused by the
new interband-pairing ansatz.

## Interpretation

The moire geometry and simple energy-unit conversion are consistent with the
old manuscript. However, the PRB table is not reproduced by the current
response engine after matching `nk`, `n_keep`, `mu`, and `Delta0`.

This means the mismatch is not a single missing global unit factor. The next
audit should focus on:

1. Kubo prefactors and possible signs/factors of 2;
2. Nambu current convention, especially hole-sector signs;
3. BZ averaging and whether the older code used a different integration weight;
4. whether the previous PRB table came from a different response implementation;
5. whether the continuum diamagnetic/regularization convention was handled
   differently in the older draft.

## Decision

Do not merge the new interband-pairing results into the manuscript's numerical
tables until the baseline response convention is reconciled. Near-term figures
should continue to use normalized mechanism quantities such as
`D_iso(eta)/D_iso(0)-1`.

## Current-Convention Audit

Command:

```text
python3 scripts/audit_response_conventions.py --nk 14 --n-keep-values 2 6 --output data/processed/response_convention_audit_nk14.csv
```

Result:

```text
n_keep=2, intra_tauz_inter_tau0: D_iso = 29.34 eV A^2, delta = -56.53%
n_keep=2, all_tauz:              D_iso = 33.45 eV A^2, delta = -50.44%
n_keep=2, all_tau0:              D_iso =  8.40 eV A^2, delta = -87.56%

n_keep=6, intra_tauz_inter_tau0: D_iso = 85.60 eV A^2,  delta = -33.79%
n_keep=6, all_tauz:              D_iso = 100.94 eV A^2, delta = -21.93%
n_keep=6, all_tau0:              D_iso = 59.88 eV A^2,  delta = -53.69%
```

The `all_tauz` current convention moves the result toward the PRB benchmark,
especially at `n_keep=6`, but it does not close the gap. The remaining mismatch
therefore likely involves additional implementation differences such as Kubo
prefactors, BZ integration, band selection details, or an older response-code
convention.

## Follow-Up Audit

See:

```text
notes/bm_prefactor_audit_result_2026-06-09.md
```

Summary:

```text
The BM geometry factors are internally consistent.
The current BM implementation gives W2 ~= 6.1 meV at theta = 1.05 deg, not the
11.2 meV quoted in the old PRB text.
Moving to theta = 1.20 deg gives W2 ~= 11.8 meV but does not fix D_iso.
No single global prefactor matches both n_keep=2 and n_keep=6.
The all_tauz geometric sector matches the PRB n_keep=6 geometric contribution,
but the conventional sector remains too small by about a factor of two.
```
