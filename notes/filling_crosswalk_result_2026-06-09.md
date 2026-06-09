# Filling Crosswalk Result

Date: 2026-06-09

Purpose:
connect the retained-band filling proxy used in the dense response table to a
central two-flat-band filling count.  This is a BM-model crosswalk for the
current numerical scan, not a device-level experimental carrier-density
calibration.

Command:

```bash
python3 scripts/build_filling_crosswalk.py
```

Output:

```text
data/processed/filling_crosswalk_nk7_nshell3.csv
```

Definition:

```text
nu_proxy = g * (<mean occupied fraction over n_keep=6>_k - 1/2)
nu_flat  = g * (<occupied central flat bands per flavor>_k - 1)
g = 4
```

Result:

```text
central flat-band window = [-1.051183, 4.133851] meV
mu = -5, -4, -3, -2 meV -> nu_flat = -4.000
mu = 0 meV -> nu_flat = -2.286
mu = 2 meV -> nu_flat = 0.735
mu = 4 meV -> nu_flat = 3.918
mu = 5 meV -> nu_flat = 4.000
```

Interpretation:

The dense chemical-potential window spans the full central two-flat-band
counting range from empty to full.  The retained-band proxy remains useful as a
monotone scan label, while `nu_flat` provides a more recognizable MATBG
flat-band filling reference.

Manuscript integration:

- Supplemental Table `tab:sm_filling_crosswalk` reports `mu`, `nu_proxy`,
  `nu_flat`, and occupied central flat bands per flavor.
- The main text now points readers to this crosswalk while preserving the
  conservative statement that no device-specific filling calibration is claimed.
