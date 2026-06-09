# Convergence Sufficiency Audit

Date: 2026-06-09

## Question

Do the current finite-grid data support the normalized-response mechanism
claim used in the PRB-targeted manuscript?

## Audit Command

```bash
python3 scripts/audit_convergence_sufficiency.py
```

Output:

```text
data/processed/convergence_sufficiency_audit.csv
```

## Result

All nine convergence-sufficiency checks pass for the current selected-grid
mechanism-paper scope.

Key values:

```text
fixed-Frobenius nk=9/11/13 key-point response range: 6.04% to 10.13%
largest per-mu nk=9/11/13 spread: 2.85 percentage points
minimum fixed-Frobenius 1/nk^2 intercept: 8.65%
minimum fixed-Frobenius 1/nk intercept: 10.82%
nk=15 fixed-Frobenius spot checks at mu=0,2 meV: 8.97%, 8.65%
largest |nk15-nk13| shift at those spot checks: 1.16 percentage points
maximum measured |fixed-Delta0 response|: 1.96%
W_inter target range across checked grids: 0.1073 to 0.1099
```

## Interpretation

The evidence is sufficient for the current selected-grid normalized mechanism
claim:

```text
the fixed-Frobenius interband-pairing response is positive and stable in sign
and scale across the checked key-point grids.
```

The evidence is not sufficient for:

```text
a final continuum-limit numerical estimate
a dense nk=15 replacement of the nk=7 mu-eta maps
a direct absolute-stiffness comparison with experiment
```

## Manuscript Consequence

The main text and Supplemental Material may state that the convergence
self-audit supports the selected-grid normalized mechanism claim.  They should
continue to avoid strict continuum-limit, absolute-stiffness, or experimental
dome-mapping claims unless those expanded-scope calculations are added.
