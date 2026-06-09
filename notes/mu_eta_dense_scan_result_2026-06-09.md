# Dense Mu-Eta Scan Result

日期：2026-06-09

## Question

Does the eta-dependent response form a coherent map across chemical potential?

## Commands

```text
python3 scripts/run_mu_response_scan.py --n-shell 3 --nk 7 --n-keep 6 --mus -5 -4 -3 -2 -1 0 1 2 3 4 5 --etas 0 0.25 0.5 0.75 1 --output data/processed/mu_eta_response_scan_nk7_nkeep6.csv

python3 scripts/plot_mu_eta_heatmap.py --input data/processed/mu_eta_response_scan_nk7_nkeep6.csv --normalization fixed_frobenius_norm --output figures/mu_eta_heatmap_nk7_nkeep6_fixed_frobenius.png

python3 scripts/plot_mu_eta_heatmap.py --input data/processed/mu_eta_response_scan_nk7_nkeep6.csv --normalization fixed_delta0 --output figures/mu_eta_heatmap_nk7_nkeep6_fixed_delta0.png

python3 scripts/summarize_eta_effect.py data/processed/mu_eta_response_scan_nk7_nkeep6.csv --output data/processed/mu_eta_response_scan_nk7_nkeep6_eta1_summary.csv
```

## Files

```text
data/processed/mu_eta_response_scan_nk7_nkeep6.csv
data/processed/mu_eta_response_scan_nk7_nkeep6_eta1_summary.csv
figures/mu_eta_heatmap_nk7_nkeep6_fixed_frobenius.png
figures/mu_eta_heatmap_nk7_nkeep6_fixed_delta0.png
```

## Result

For `eta=1` relative to `eta=0`, fixed-Frobenius normalization gives:

```text
mu = -5 meV ->  +0.56%
mu = -4 meV ->  +8.91%
mu = -3 meV ->  +7.85%
mu = -2 meV ->  +5.37%
mu = -1 meV ->  +8.02%
mu =  0 meV ->  +8.17%
mu =  1 meV ->  +9.14%
mu =  2 meV ->  +9.49%
mu =  3 meV ->  +6.53%
mu =  4 meV ->  +6.62%
mu =  5 meV -> +11.86%
```

Fixed-Delta0 normalization is much weaker and can be negative:

```text
range: about -5.10% to +3.12%
```

## nk=9 Key-Point Check

Command:

```text
python3 scripts/run_mu_response_scan.py --n-shell 3 --nk 9 --n-keep 6 --mus -4 0 2 4 --etas 0 0.5 1 --output data/processed/mu_response_scan_nk9_nkeep6_keypoints.csv

python3 scripts/summarize_eta_effect.py data/processed/mu_response_scan_nk9_nkeep6_keypoints.csv --output data/processed/mu_response_scan_nk9_nkeep6_keypoints_summary.csv
```

For `eta=1` relative to `eta=0`, fixed-Frobenius gives:

```text
mu = -4 meV -> +6.04%
mu =  0 meV -> +8.63%
mu =  2 meV -> +6.43%
mu =  4 meV -> +6.05%
```

Fixed-Delta0 remains small:

```text
mu = -4 meV -> -0.68%
mu =  0 meV -> +1.03%
mu =  2 meV -> -0.29%
mu =  4 meV -> -0.17%
```

## Interpretation

The dense scan supports the following working conclusion:

```text
The orbital-projected interband-pairing direction produces a reproducible normalized D_iso response across chemical potential in fixed-Frobenius mode, while fixed-Delta0 largely suppresses the effect.
```

This is a normalization-conditioned mechanism signature, not yet a direct experimental prediction.

## Filling Proxy

The scan now includes:

```text
nu_proxy
```

This is a normal-state retained-band occupancy proxy, not a final experimental filling calibration. It is useful for plotting and rough comparison, but should be replaced or calibrated before final manuscript claims.

## Next Step

Before expanding the grid further:

1. implement physical-unit conversion options;
2. compare the `eta=0` baseline with the existing manuscript convention;
3. decide whether fixed-Frobenius or fixed-Delta0 is the main-text scan.
