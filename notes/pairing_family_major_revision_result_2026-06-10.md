# Pairing-Family Major-Revision Result

Date: 2026-06-10

## Purpose

This note records the first response to the review criticism that the current
manuscript relies too strongly on one working orbital ansatz
`M1=taux_sigmax`.  The test asks whether the normalized response signature
appears across a small family of real symmetric layer-sublattice orbital
directions.

## Command

```bash
python3 scripts/run_pairing_family_response_scan.py
python3 scripts/plot_pairing_family_response.py
```

## Scope

This is a first-pass family scan at:

```text
nk = 7
n_keep = 6
n_shell = 3
mu = -4, 0, 2, 4 meV
eta = 0, 1
normalizations = fixed_frobenius_norm, fixed_delta0
partner = tr_sewn
```

It is not yet a replacement for the planned grid, truncation, shell, or
valley-sewing robustness audits.

## Outputs

```text
data/processed/pairing_family_response_scan.csv
data/processed/pairing_family_response_summary.csv
data/processed/pairing_family_response_audit.csv
figures/pairing_family_response_summary.png
figures/pairing_family_response_summary.pdf
```

## Main Finding

All eight candidate directions show positive fixed-Frobenius response changes
at all four sampled chemical potentials.  Across the family, the
fixed-Frobenius response ranges from about `+6.43%` to `+9.49%`.

The fixed-Delta0 control remains weak and convention-sensitive: it ranges from
about `-1.46%` to `+2.91%`, with several directions changing sign over the
sampled chemical potentials.

## Direction-Level Summary

| M1 | fixed-Frobenius range (%) | fixed-Delta0 range (%) | mean W_inter |
|---|---:|---:|---:|
| tau0_sigmax | 7.09 to 9.05 | -0.31 to 1.50 | 0.0179 |
| tau0_sigmaz | 7.30 to 9.06 | -0.04 to 0.57 | 0.0422 |
| taux_sigma0 | 6.56 to 8.52 | -1.46 to 1.25 | 0.0488 |
| taux_sigmax | 6.62 to 9.49 | -0.05 to 2.91 | 0.1082 |
| taux_sigmaz | 7.47 to 8.71 | 0.16 to 0.23 | 0.0374 |
| tauz_sigma0 | 7.19 to 8.37 | -0.21 to 0.14 | 0.0050 |
| tauz_sigmax | 6.43 to 9.17 | -1.09 to 1.64 | 0.1304 |
| tauz_sigmaz | 7.33 to 8.77 | 0.01 to 0.18 | 0.0109 |

## Interpretation

The current `M1=taux_sigmax` direction is not the only direction showing the
fixed-Frobenius normalized response signature.  The first-pass family scan
therefore supports reframing the main result as a feature of a tested
orbital-pairing family, not merely a single successful ansatz.

However, this evidence is still at the original dense-map grid and shell
choice.  The manuscript should not yet claim full PRB-level robustness until
the same family-level conclusion is tested against higher `nk`, retained-band
truncation, moire-shell cutoff, and valley-sewing choices.

## Audit Status

The first-pass pairing-family audit is run with:

```bash
python3 scripts/audit_pairing_family_response.py
```

It currently passes all seven checks: the scan includes eight candidate
directions, all scanned matrices are real/symmetric/Hermitian, the original
`taux_sigmax` direction is included, all fixed-Frobenius rows are positive, the
minimum fixed-Frobenius response exceeds five percent, the fixed-Delta0 control
has sign sensitivity, and the fixed-Delta0 response remains less than half the
weakest fixed-Frobenius response in absolute magnitude.
