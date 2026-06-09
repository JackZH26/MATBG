# Observable Policy Decision

Date: 2026-06-09

## Question

Should the current PRB-targeted manuscript report claim-bearing absolute
superfluid stiffness values, or should it restrict the main claims to
normalized response diagnostics?

## Evidence

The production interband-pairing response engine uses the finite-band
diagnostic current split implemented in `src/matbg/stiffness.py`:

```text
intraband velocity current: tau_z
interband velocity current: tau_0
```

The benchmark reconstruction scripts show that the prior band-basis
decomposition table is not reproduced by a single global prefactor or one
uniform response convention:

```text
current tau_z/tau_0 route:
  n_keep=2 D_iso = 29.34 eV A^2 vs 67.50 target
  n_keep=6 D_iso = 85.60 eV A^2 vs 129.30 target

double_conv_all_tauz route:
  n_keep=6 D_total = 126.66 eV A^2 vs 129.30 target
  n_keep=2 D_total = 54.40 eV A^2 vs 67.50 target

gamma-centered flat endpoint audit:
  n_keep=2 D_total = 66.18 eV A^2 vs 67.50 target
  but the same full-curvature correction does not work cleanly at n_keep=6
```

The normalized response signal is much more stable across the current
evidence base:

```text
fixed-Frobenius eta=1 response over mu=-5...5 meV: +0.56% to +11.86%
nk=9/11/13 selected-grid checks: positive fixed-Frobenius sign
nk=15 spot check at mu=0,2 meV: +8.97%, +8.65%
fixed-Delta0 control: weak and sign-sensitive
```

## Decision

For the current PRB mechanism-paper scope, the claim-bearing observable is:

```text
D_iso(mu, eta) / D_iso(mu, eta=0) - 1
```

with `fixed_frobenius_norm` as the primary mechanism scan and `fixed_delta0` as
the control.

Raw response values are internal finite-band diagnostics. eV A^2 per-flavor
values are allowed only in benchmark self-audit tables and provenance
discussion. They are not final experimental stiffness predictions.

## Manuscript Consequences

Allowed:

```text
normalized finite-band response mechanism signature
channel redistribution diagnostics
benchmark provenance for old absolute tables
```

Not allowed:

```text
claim-bearing absolute stiffness values
direct quantitative agreement with experimental stiffness
device-level superconducting-dome comparison
```

## Future Scope Expansion

If a later manuscript version adds direct experimental comparison, it must
regenerate absolute values from one declared response convention with explicit:

```text
spin/valley degeneracy
Brillouin-zone or moire-cell normalization
Nambu-current convention
diamagnetic or curvature regularization
band-selection and mesh convention
```

That future task is separate from the current normalized-response mechanism
paper.

## Guardrail

The policy is checked by:

```bash
python3 scripts/audit_observable_policy.py
```

which writes:

```text
data/processed/observable_policy_audit.csv
```
