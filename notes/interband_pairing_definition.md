# Interband Pairing Definition Note

日期：2026-06-07  
状态：Sprint 1 working note  
关联计划：`MATBG_Executable_Research_Plan_2026.md`

## 1. Purpose

The proposal defines interband pairing as pairing whose matrix in the normal-state band basis contains nonzero off-diagonal elements:

```text
intraband:  Delta_nm(k) = 0 for n != m
interband:  Delta_nm(k) != 0 for at least some n != m
```

This is the correct diagnostic language, but it is not yet a complete physical ansatz. In a band basis, eigenvectors can be rephased independently:

```text
|u_n(k)> -> exp(i phi_n(k)) |u_n(k)>
```

Therefore, an arbitrary constant off-diagonal term such as `Delta_12(k) = eta Delta0` can become gauge dependent unless its transformation rule is specified. A gauge-dependent pairing ansatz can generate stiffness differences that are artifacts of eigenvector convention rather than physical signatures.

## 2. Principle

The main calculation should use a gauge-covariant construction:

```text
Define pairing in orbital/sublattice/layer basis first.
Project it into the band basis using normal-state eigenvectors.
Measure interband content after projection.
```

The working formula is:

```text
Delta_band(k) = U^\dagger(k) Delta_orb(k) U^*(-k)
```

where `U(k)` diagonalizes the normal-state BM Hamiltonian:

```text
H_BM(k) U(k) = U(k) epsilon(k)
```

Under a band-basis gauge change, `Delta_band(k)` transforms covariantly, while BdG spectra and total stiffness observables remain invariant.

## 3. Route A: Orbital-Defined Pairing

This is the preferred route.

### 3.1 Baseline intra-like pairing

Start from an orbital/layer/sublattice matrix that reproduces the already benchmarked uniform s-wave behavior after projection:

```text
Delta_orb^0(k) = Delta0 M0
```

where `M0` is local and symmetry-compatible.

Expected behavior:

1. Projection produces mostly band-diagonal pairing in the flat-band subspace.
2. `eta = 0` should reproduce the existing uniform s-wave benchmark within numerical tolerance.

### 3.2 Interband-enhanced pairing

Introduce a second orbital matrix:

```text
Delta_orb(k; eta) = Delta0 normalize[M0 + eta M1]
```

where `M1` is chosen to enhance off-diagonal band-basis components after projection.

Initial scan values:

```text
eta = 0.00, 0.10, 0.25, 0.50, 0.75, 1.00
```

The normalization must be explicit. Two complementary scans are required:

1. fixed `Delta0` scan, to see raw stiffness response;
2. fixed projected gap norm scan, to separate gap-size effects from pairing-structure effects.

### 3.3 Interband weight diagnostic

For each `k`, define a diagnostic off-diagonal weight:

```text
W_inter(k) = sum_{n != m} |Delta_nm(k)|^2 / sum_{n,m} |Delta_nm(k)|^2
```

Then report Brillouin-zone average:

```text
<W_inter>_BZ
```

This diagnostic is not a direct observable, but it verifies that `eta` actually tunes interband content.

## 4. Route B: Band-Basis Phenomenology

Use only as fallback.

Minimum requirements:

1. Define how `Delta_nm(k)` transforms under `|u_n(k)> -> exp(i phi_n(k)) |u_n(k)>`.
2. Implement a smooth gauge or parallel-transport gauge.
3. Run random phase tests on `U(k)`.
4. Confirm that `Dxx_total`, `Dyy_total`, and BdG eigenvalues are unchanged.

If total observables change under random rephasing, the ansatz is invalid for main-text conclusions.

## 5. Required Tests Before Scans

### 5.1 Hermiticity

BdG Hamiltonian must satisfy:

```text
H_BdG(k) = H_BdG^\dagger(k)
```

### 5.2 Particle-hole symmetry

The spectrum must appear in positive and negative pairs:

```text
E_a(k) = -E_b(-k)
```

within numerical tolerance.

### 5.3 Pairing symmetry

For the spin-singlet even-parity channel, check:

```text
Delta(k) = Delta^T(-k)
```

For any later triplet or valley-structured channel, write the appropriate antisymmetry rule explicitly before implementation.

### 5.4 Gauge randomization

Apply random phases to the band eigenvectors:

```text
U(k) -> U(k) diag(exp(i phi_n(k)))
```

Then recompute:

```text
BdG eigenvalues
Dxx_total
Dyy_total
```

Acceptance:

```text
relative change < 1e-8 for spectra
relative change < 1e-6 for stiffness observables
```

Tolerances can be relaxed only if the numerical source is documented.

## 6. Gate 1 Decision

Deadline: 2026-06-13.

Go:

1. Route A or Route B is fixed.
2. `Delta(k)` is written explicitly.
3. Tests 5.1 to 5.4 pass.
4. `eta` demonstrably tunes `<W_inter>_BZ`.

No-Go:

1. Stop large parameter scans.
2. Replace arbitrary band-basis ansatz with orbital-projected ansatz.
3. Record the failed ansatz as a methodological caution, not as physics.

## 7. Immediate Open Choices

The next research choice is the concrete orbital matrix pair `(M0, M1)`.

Current candidate strategy:

1. `M0`: identity-like local spin-singlet pairing in the retained orbital basis, `tau0_sigma0`.
2. `M1`: layer-sublattice mixed pairing, `taux_sigmax`, chosen after the first BM projection screen.
3. Compare the projected off-diagonal weight before running stiffness scans.

This choice should be checked with an explicit valley-basis sewing convention before writing production stiffness scan code. The `conjugate_k` proxy is useful for algebraic validation, but it is not a substitute for a fully documented valley pairing convention.
