# Valley-Sewing Response Sensitivity

Date: 2026-06-10

## Purpose

This note records the response-level valley-partner sensitivity test requested
by the PRB-style review.  The previous manuscript already documented that the
production calculation uses a `tr_sewn` convention, but the review correctly
identified that this convention is part of the physics interpretation rather
than a peripheral implementation detail.

## Commands

```bash
python3 scripts/run_valley_sewing_response_sensitivity.py
python3 scripts/audit_valley_sewing_response_sensitivity.py
python3 scripts/plot_valley_sewing_response_sensitivity.py
```

## Scope

The scan keeps the same finite-band response formula and changes only the
paired-sector partner vectors used to project the orbital pairing matrix:

```text
partners = tr_sewn, same_valley, time_reversed_valley, sewn_time_reversed_valley
nk       = 9, 13, 15
n_shell  = 3, 4
n_keep   = 6
mu       = -4, 0, 2, 4 meV
eta      = 0, 1
normalizations = fixed_frobenius_norm, fixed_delta0
```

This is a sensitivity diagnostic, not a replacement for a fully independent
two-valley response implementation.

## Outputs

```text
data/processed/valley_sewing_response_sensitivity.csv
data/processed/valley_sewing_response_sensitivity_summary.csv
data/processed/valley_sewing_response_sensitivity_audit.csv
figures/valley_sewing_response_sensitivity.png
figures/valley_sewing_response_sensitivity.pdf
```

The raw scan contains `384` rows.  The eta=1 versus eta=0 summary contains
`192` rows.

## Main Result

The working `tr_sewn` convention remains internally stable:

```text
tr_sewn fixed-Frobenius: 24/24 positive
range: +4.374% to +13.603%
mean:  +9.182%
max particle-hole spectrum error: 0
```

Alternative partner choices are strongly convention-sensitive:

```text
same_valley fixed-Frobenius:              14/24 positive
time_reversed_valley fixed-Frobenius:     12/24 positive
sewn_time_reversed_valley fixed-Frobenius: 8/24 positive
```

The alternative partner choices also show measurable particle-hole spectrum
errors in the finite-band BdG diagnostic:

```text
same_valley max PH error:              3.731e-02
time_reversed_valley max PH error:     2.672e-02
sewn_time_reversed_valley max PH error: 2.064e-02
```

The largest partner-convention spread in the fixed-Frobenius response is
`63.973` percentage points.

## Interpretation

This sensitivity test does not support claiming that the normalized response
signature is valley-sewing independent.  Instead, it supports a sharper and
more defensible PRB framing:

1. The production response claim is tied to the explicitly declared `tr_sewn`
   finite-band diagnostic convention.
2. Alternative raw or Procrustes-sewn partner choices are useful stress tests,
   but they are not PH-consistent replacement production conventions in the
   present one-valley response implementation.
3. A future valley-asymmetric or device-level theory must use a fully
   independent two-valley implementation before making valley-basis-independent
   stiffness claims.

## Manuscript Implication

The revised manuscript should move the valley-sewing discussion from a soft
limitation to a central claim-scope boundary.  A suitable statement is:

```text
The positive normalized response is robust within the declared `tr_sewn`
finite-band diagnostic convention, but the response is not presently claimed
to be independent of valley-partner basis choices.  Alternative partner choices
act as stress tests and expose sign and particle-hole-symmetry sensitivity,
which is why a fully independent two-valley implementation is deferred.
```

This is a stronger revision than simply saying that valley sewing remains
future work, because it quantifies the sensitivity and prevents the paper from
overclaiming basis-independent physics.
