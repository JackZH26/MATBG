# nk=11 Key-Point Convergence Result

Date: 2026-06-09

## Question

Does the normalization-conditioned interband-pairing response survive a higher
momentum-grid key-point check beyond the existing `nk=9` validation?

## Commands

```bash
python3 scripts/run_mu_response_scan.py \
  --nk 11 \
  --n-shell 3 \
  --n-keep 6 \
  --mus -4 0 2 4 \
  --etas 0 0.5 1 \
  --output data/processed/mu_response_scan_nk11_nkeep6_keypoints.csv

python3 scripts/summarize_eta_effect.py \
  data/processed/mu_response_scan_nk11_nkeep6_keypoints.csv \
  --output data/processed/mu_response_scan_nk11_nkeep6_keypoints_summary.csv
```

Config:
`configs/mu_response_convergence_nk11.yaml`

## Result

The `eta=1` response relative to `eta=0` is:

| normalization | mu (meV) | nk=9 | nk=11 | nk11 - nk9 |
|---|---:|---:|---:|---:|
| fixed_delta0 | -4 | -0.0068 | -0.0061 | +0.0007 |
| fixed_delta0 | 0 | +0.0103 | +0.0080 | -0.0023 |
| fixed_delta0 | 2 | -0.0029 | +0.0118 | +0.0147 |
| fixed_delta0 | 4 | -0.0017 | -0.0003 | +0.0014 |
| fixed_frobenius_norm | -4 | +0.0604 | +0.0617 | +0.0012 |
| fixed_frobenius_norm | 0 | +0.0863 | +0.0796 | -0.0067 |
| fixed_frobenius_norm | 2 | +0.0643 | +0.0927 | +0.0285 |
| fixed_frobenius_norm | 4 | +0.0605 | +0.0608 | +0.0002 |

The fixed-Frobenius response remains positive at all four key points:

```text
mu = -4 meV -> +6.17%
mu =  0 meV -> +7.96%
mu =  2 meV -> +9.27%
mu =  4 meV -> +6.08%
```

The fixed-Delta0 response remains small and sign-sensitive.

## Interpretation

The higher-grid key-point check strengthens the qualitative mechanism claim:
the fixed-Frobenius interband-pairing response is not an artifact of the
`nk=7` dense grid or the `nk=9` validation grid.

However, the pointwise values are not fully converged in a strict extrapolation
sense. The largest `nk=11 - nk=9` shift occurs at `mu=2 meV` in the
fixed-Frobenius mode, where the relative response changes by about `+2.85`
percentage points. Therefore the manuscript should claim robust sign and
order-of-magnitude stability, not final continuum-limit numerical values.

## Decision

1. Update the Supplemental Material with an `nk=9` versus `nk=11` convergence
   table.
2. Update the readiness audit: the previous `nk=11` gate is now partially
   satisfied, but a final submission should still avoid continuum-extrapolated
   numerical claims unless a denser extrapolation is performed.
