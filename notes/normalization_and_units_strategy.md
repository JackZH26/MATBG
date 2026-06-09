# Normalization and Units Strategy

日期：2026-06-09

## 1. Current Status

Current response outputs are gate-level finite-band diagnostics:

```text
Dxx_total_raw
Dyy_total_raw
Dconv_raw
Dgeom_raw
Dcross_raw
```

They are computed from the finite-band BdG paramagnetic Kubo expression in the retained band subspace.

They currently do **not** include:

1. moire-cell area normalization;
2. spin/valley degeneracy factor;
3. continuum-model diamagnetic counterterm or lattice regularization;
4. experimental unit conversion;
5. self-consistent gap normalization.

Therefore, raw values should not be compared directly to experiment or to the existing PRB table.

## 2. Three-Layer Reporting Convention

### Layer A: Raw Gate Response

Use for code debugging and internal checks:

```text
Dxx_total_raw
Dyy_total_raw
Dxx_conv_raw
Dxx_geom_raw
Dxx_cross_raw
```

Allowed claims:

```text
The response engine closes numerically.
The response varies smoothly with eta/mu.
The conv/geom/cross decomposition is internally consistent.
```

Not allowed:

```text
This raw number is the physical superfluid stiffness.
```

### Layer B: Normalized Mechanism Response

Use for main near-term figures:

```text
D_iso(mu, eta) / D_iso(mu, eta=0) - 1
Dgeom / Dtotal
Dxx / Dyy
W_inter
```

This layer is appropriate for the first manuscript-level mechanism maps because it reduces sensitivity to missing global prefactors.

### Layer C: Physical Units

Use only after adding:

```text
moire area factor
spin/valley degeneracy
clear current convention
lattice or cutoff regularization discussion
```

This layer is required before quantitative comparison to experimental stiffness or kinetic inductance.

## 3. Gap Normalization Controls

Two normalization modes must remain in all scans:

```text
fixed_frobenius_norm
fixed_delta0
```

Interpretation:

1. `fixed_frobenius_norm`: controls the norm of the orbital pairing matrix direction. This is useful for scanning pairing structure.
2. `fixed_delta0`: keeps the raw gap amplitude fixed. This is closer to asking whether changing orbital structure alone modifies the response at the same input amplitude.

Current result:

```text
fixed_frobenius_norm gives a visible response enhancement.
fixed_delta0 gives a much weaker response, sometimes slightly negative.
```

Therefore, the paper must not claim unconditional stiffness enhancement from interband pairing. It should state the normalization convention whenever discussing eta trends.

## 4. Recommended Main-Figure Quantities

Primary:

```text
relative D_iso enhancement: D_iso(eta)/D_iso(0)-1
projected interband pairing weight: W_inter
```

Secondary:

```text
geometric fraction
Dconv, Dgeom, Dcross
```

Defer:

```text
absolute D values in physical units
anisotropy as a main signature
```

Anisotropy remains useful as a diagnostic, but current scans do not support it as the primary observable signature.

## 5. Next Unit-Conversion Tasks

1. Define the exact moire-cell area used by the BM model.
2. Decide whether the response should be divided by the sampled Brillouin-zone area or moire-cell area.
3. Add spin/valley degeneracy as an explicit optional factor.
4. Compare the `eta=0` baseline against the existing PRB manuscript values only after the same conventions are matched.
