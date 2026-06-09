# PRB Table Reconstruction Result

日期：2026-06-09

## Question

Can the old PRB uniform-s benchmark table be reconstructed by an explicit,
auditable pipeline separate from the interband-pairing mechanism scans?

## Command

```text
python3 scripts/reconstruct_prb_table.py --nk 14 --n-keep-values 2 4 6 --output data/processed/prb_table_reconstruction_nk14.csv
```

Target values are stored in:

```text
data/processed/prb_manuscript_targets.csv
```

## Candidate Definitions

```text
current_tauz_tau0:
  conventional = intraband tau_z current-current response
  geometric    = interband tau_0 current-current response

all_tauz:
  conventional = intraband tau_z current-current response
  geometric    = interband tau_z current-current response

double_conv_all_tauz:
  conventional = 2 * intraband tau_z current-current response
  geometric    = interband tau_z current-current response

double_conv_half_curv_all_tauz:
  conventional = 2 * intraband tau_z current-current response + 0.5 curvature term
  geometric    = interband tau_z current-current response
```

## Best Unified Candidate

The best simple unified reconstruction is:

```text
double_conv_all_tauz
```

It gives:

```text
n_keep = 2:
D_total = 54.40 vs target 67.50 eV A^2  (-19.41%)
D_conv  = 41.89 vs target 53.00 eV A^2  (-20.96%)
D_geom  = 12.50 vs target 14.50 eV A^2  (-13.76%)

n_keep = 4:
D_conv  = 50.78 vs target 53.90 eV A^2  (-5.79%)

n_keep = 6:
D_total = 126.66 vs target 129.30 eV A^2 (-2.04%)
D_conv  =  51.45 vs target 54.00 eV A^2  (-4.73%)
D_geom  =  75.22 vs target 75.30 eV A^2  (-0.11%)
```

This candidate nearly reconstructs the extended-band endpoint (`n_keep=6`) and
the intermediate conventional value (`n_keep=4`), but it does not reconstruct
the flat-band endpoint (`n_keep=2`).

## Curvature Candidate

Adding a half-curvature term improves `n_keep=2` but worsens `n_keep=6`:

```text
double_conv_half_curv_all_tauz:

n_keep = 2:
D_total = 62.45 vs target 67.50 eV A^2 (-7.49%)
D_conv  = 49.94 vs target 53.00 eV A^2 (-5.77%)

n_keep = 6:
D_total = 136.14 vs target 129.30 eV A^2 (+5.29%)
D_conv  =  60.92 vs target 54.00 eV A^2  (+12.82%)
```

Therefore a curvature correction is not a clean universal reconstruction.

## Decision

The old PRB table is partially reproducible by the explicit
`double_conv_all_tauz` convention, especially once remote bands are included.
The remaining discrepancy is concentrated at `n_keep=2`.

Do not edit the production interband-pairing response convention to match the
old table. Keep the PRB reconstruction as a separate benchmark route, and use
normalized eta-response quantities for new mechanism claims until the
flat-band endpoint is fully understood.

## Flat-Band Endpoint Follow-Up

See:

```text
notes/flatband_endpoint_audit_result_2026-06-09.md
```

The closest audited `n_keep=2` reconstruction uses:

```text
gamma_centered mesh
central_pair band selector
double_conv_full_curv_all_tauz
```

and gives:

```text
D_total = 66.18 vs 67.50 eV A^2
D_conv  = 53.83 vs 53.00 eV A^2
D_geom  = 12.36 vs 14.50 eV A^2
```

This nearly reconstructs the old flat-band total and conventional values, but
the geometric component remains low and the same full-curvature correction does
not work cleanly at `n_keep=6`.
