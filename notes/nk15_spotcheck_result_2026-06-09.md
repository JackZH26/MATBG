# nk15 Spot-Check Result

Date: 2026-06-09

Purpose:
add a higher-grid representative spot check beyond the selected `nk=9/11/13`
key-point convergence and finite-grid trend audit.

Commands:

```bash
python3 scripts/run_mu_response_scan.py \
  --nk 15 --n-shell 3 --n-keep 6 \
  --mus 0 2 --etas 0 1 \
  --output data/processed/mu_response_scan_nk15_nkeep6_spotcheck.csv

python3 scripts/summarize_eta_effect.py \
  data/processed/mu_response_scan_nk15_nkeep6_spotcheck.csv \
  --output data/processed/mu_response_scan_nk15_nkeep6_spotcheck_summary.csv
```

Outputs:

```text
data/processed/mu_response_scan_nk15_nkeep6_spotcheck.csv
data/processed/mu_response_scan_nk15_nkeep6_spotcheck_summary.csv
```

Result:

```text
fixed Frobenius, mu=0 meV: +8.9718%
fixed Frobenius, mu=2 meV: +8.6506%
fixed Delta0, mu=0 meV: +0.8463%
fixed Delta0, mu=2 meV: +0.7092%
W_inter(eta=1): 0.1076
max particle-hole spectrum error: 1.8e-15
```

Interpretation:

The `nk=15` spot check preserves a positive fixed-Frobenius response at the two
representative chemical potentials and keeps the response in the same range as
the `nk=13` key-point values.  The fixed-Delta0 control remains much smaller.
This strengthens the finite-grid stability claim, but it is still a targeted
spot check rather than a complete continuum-grid extrapolation.
