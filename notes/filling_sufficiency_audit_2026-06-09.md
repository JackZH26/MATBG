# Filling Sufficiency Audit

Date: 2026-06-09

## Question

Is the current central-flat-band crosswalk sufficient for the PRB mechanism
paper, without adding a device-level carrier-density calibration?

## Audit Command

```bash
python3 scripts/audit_filling_sufficiency.py
```

Output:

```text
data/processed/filling_sufficiency_audit.csv
```

## Result

All nine filling-sufficiency checks pass for the current mechanism-paper scope.

Key values:

```text
crosswalk mu grid matches the dense response summary: 11/11 values
nu_proxy range: -1.483 to 0.857, strictly increasing
nu_flat range: -4.000 to 4.000, nondecreasing
dense mu range: [-5.000, 5.000] meV
central two-flat-band window: [-1.051, 4.134] meV
occupied central flat bands per flavor: 0.000 to 2.000
closest sampled |nu_flat|: 0.327
closest sampled distance to nu_flat=-2: 0.286
closest sampled distance to nu_flat=+2: 0.367
```

## Interpretation

The evidence is sufficient for using the crosswalk as a BM central-flat-band
counting reference for the dense response maps.  It supports statements that
the scan spans the central two-flat-band manifold and includes counting
reference points near common MATBG fillings such as `nu_flat=0` and
`nu_flat=+-2`.

The evidence is not sufficient for:

```text
a device-level carrier-density calibration
a quantitative superconducting-dome map
experimental filling assignment for a specific sample
```

## Manuscript Consequence

The main text and Supplemental Material may now treat the central-flat-band
crosswalk as sufficient for the current mechanism-paper filling reference.
They should continue to state that direct comparison to experimental dome
locations requires a separate device-level calibration.
