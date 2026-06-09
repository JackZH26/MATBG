# Valley Sewing Convention

日期：2026-06-07  
状态：Gate 1.5 decision note

## Problem

The projected pairing diagnostic depends on a comparison between paired normal-state band bases:

```text
Delta_band(k) = U_+^\dagger(k) Delta_orb U_-^*(-k)
```

The raw eigenvectors returned independently for valley `+` and valley `-` are not automatically in the same time-reversal sewing convention. As a result, even a trivial orbital identity pairing,

```text
M0 = tau0_sigma0
```

can appear highly band-off-diagonal if the two valley eigenvector gauges are not aligned.

## Diagnostic Result

The raw `valley=-1` implementation was compared against the identity-orbital time-reversal target:

```text
U_-(-k) target = U_+(k)^*
```

Using Procrustes alignment within the retained subspace gives poor overlap for the current raw valley-minus BM convention:

```text
n_keep = 2 -> min singular value about 0.022
n_keep = 4 -> min singular value about 0.004
n_keep = 6 -> min singular value about 0.002
```

The alignment residual is large, about `1.38` to `1.39`. This means raw valley-minus eigenvectors should not be used directly for the pairing off-diagonal diagnostic.

## Working Convention

For the next executable stage, use:

```text
partner = tr_sewn
U_-(-k) := U_+(k)^*
```

This defines the time-reversed valley partner in the same orbital basis. It is equivalent to choosing a valley basis in which the spinless time-reversal operator is complex conjugation on the orbital components.

This convention is appropriate for the current restricted goal:

1. define a gauge-covariant pairing ansatz;
2. measure whether the orbital matrix creates band-off-diagonal content;
3. avoid false off-diagonal weight from arbitrary valley eigenvector gauges.

## Caveat

`tr_sewn` is a convention choice, not a full independent construction of the valley-minus continuum Hamiltonian. Before final manuscript claims, the methods section must state the sewing convention explicitly. If the project later includes valley-asymmetric perturbations, strain, or valley-dependent interactions, this convention must be revisited.

## Implementation

`scripts/run_bm_pairing_projection_gate.py` supports:

```text
--partner tr_sewn
```

This is now the default.

Raw diagnostic modes remain available:

```text
--partner time_reversed_valley
--partner sewn_time_reversed_valley
```

These modes should be used only to diagnose gauge mismatch, not to make physics claims about interband pairing weight.

## Manuscript Integration

As of the PRB checkpoint on 2026-06-09, the main manuscript explicitly writes
the production projection as

```text
Delta_band(k) = U_+^\dagger(k) Delta_orb U_-^*(-k),
U_-(-k) = U_+^*(k),
```

so the actual `tr_sewn` scan evaluates

```text
Delta_band(k) = U_+^\dagger(k) Delta_orb U_+(k).
```

The Supplemental Material now includes a CSV-verified raw-valley diagnostic
table showing that independently diagonalized valley-minus eigenvectors have
large alignment error and very small singular values relative to the
`U_+^*(k)` target. This supports the decision not to use raw valley-minus
eigenvectors for `W_inter`.

Remaining limitation:
the current production convention is an explicitly stated diagnostic sewing
choice. A future fully independent two-valley implementation remains necessary
before studying valley-asymmetric perturbations, strain, or explicitly
valley-dependent interactions.
