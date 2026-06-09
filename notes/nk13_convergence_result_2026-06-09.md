# nk=13 Key-Point Convergence Result

Date: 2026-06-09

## Question

Does the fixed-Frobenius interband-pairing response remain positive after a
third selected momentum-grid check at `nk=13`?

## Commands

```bash
python3 scripts/run_mu_response_scan.py \
  --nk 13 \
  --n-shell 3 \
  --n-keep 6 \
  --mus -4 0 2 4 \
  --etas 0 0.5 1 \
  --output data/processed/mu_response_scan_nk13_nkeep6_keypoints.csv

python3 scripts/summarize_eta_effect.py \
  data/processed/mu_response_scan_nk13_nkeep6_keypoints.csv \
  --output data/processed/mu_response_scan_nk13_nkeep6_keypoints_summary.csv
```

Config:
`configs/mu_response_convergence_nk13.yaml`

## Result

The `eta=1` response relative to `eta=0` is:

| normalization | mu (meV) | nk=9 | nk=11 | nk=13 | nk13 - nk9 |
|---|---:|---:|---:|---:|---:|
| fixed_delta0 | -4 | -0.0068 | -0.0061 | +0.0122 | +0.0191 |
| fixed_delta0 | 0 | +0.0103 | +0.0080 | +0.0196 | +0.0093 |
| fixed_delta0 | 2 | -0.0029 | +0.0118 | +0.0024 | +0.0053 |
| fixed_delta0 | 4 | -0.0017 | -0.0003 | +0.0011 | +0.0029 |
| fixed_frobenius_norm | -4 | +0.0604 | +0.0617 | +0.0872 | +0.0267 |
| fixed_frobenius_norm | 0 | +0.0863 | +0.0796 | +0.1013 | +0.0150 |
| fixed_frobenius_norm | 2 | +0.0643 | +0.0927 | +0.0805 | +0.0162 |
| fixed_frobenius_norm | 4 | +0.0605 | +0.0608 | +0.0772 | +0.0166 |

The fixed-Frobenius response remains positive at all four key points and all
three checked grids. At `nk=13`, the positive responses are:

```text
mu = -4 meV -> +8.72%
mu =  0 meV -> +10.13%
mu =  2 meV -> +8.05%
mu =  4 meV -> +7.72%
```

## Interpretation

The `nk=13` layer strengthens the sign-stability claim for the normalized
interband-pairing mechanism. The fixed-Frobenius response is positive at every
checked key point from `nk=9` through `nk=13`.

The data still do not constitute a continuum-grid extrapolation. The largest
`nk=13 - nk=9` fixed-Frobenius shift is about `+2.67` percentage points. The
paper should therefore claim robust sign and scale over selected grids, not
final continuum-limit numerical values.

## Decision

1. Update the Supplemental Material convergence table to include `nk=13`.
2. Treat the selected-grid convergence gate as substantially strengthened.
3. Leave a final-submission caveat for strict extrapolation or denser-mesh
   saturation if absolute numerical precision becomes central to the claim.
