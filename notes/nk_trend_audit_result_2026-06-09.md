# Finite-Grid Trend Audit Result

Date: 2026-06-09

Purpose:
audit whether the selected `nk=9/11/13` key-point convergence data support the
sign stability of the normalized interband-pairing mechanism signal beyond a
visual grid-by-grid comparison.

Command:

```bash
python3 scripts/analyze_nk_trend.py
```

Outputs:

```text
data/processed/nk_trend_audit_nkeep6.csv
figures/nk_trend_audit_nkeep6.png
figures/nk_trend_audit_nkeep6.pdf
```

Method:

The audit fits the measured key-point percentage response

```text
y = 100 * [D_iso(eta=1) / D_iso(eta=0) - 1]
```

to `y(nk) = y0 + a/nk^2`.  A second `1/nk` fit is stored as a simple
sensitivity check.  Since only three grids are available, the intercepts are
not treated as a final continuum-limit estimate.

Result:

```text
fixed Frobenius h2 intercepts: 8.65% to 10.58%
fixed Frobenius h1 intercepts: 10.82% to 13.77%
fixed Delta0 measured signs: mixed except at mu = 0 meV
largest measured fixed-Frobenius range over nk=9/11/13: 6.43% to 9.27%
```

Interpretation:

The finite-grid trend audit strengthens the claim that the fixed-Frobenius
mechanism signal has stable positive sign at the selected key points.  It does
not remove the need for a denser or more formal continuum extrapolation before
making final absolute or continuum-limit claims.
