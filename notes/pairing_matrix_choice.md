# Pairing Matrix Choice for Gate 1

日期：2026-06-07  
状态：first executable choice

## 1. Basis Convention

For the first implementation, use an internal layer-sublattice basis:

```text
0 = top,    A
1 = top,    B
2 = bottom, A
3 = bottom, B
```

For a BM basis with multiple moire reciprocal vectors, assume the working order:

```text
(G_1 internal block), (G_2 internal block), ...
```

Then an internal matrix `M_internal` is expanded as:

```text
M_orbital = I_G kron M_internal
```

If the production BM code uses a different ordering, this expansion must be adapted before using the matrix in scans.

## 2. Pauli-Matrix Notation

Use:

```text
tau_i    layer Pauli matrix
sigma_i  sublattice Pauli matrix
```

with internal matrices written as:

```text
M = tau_i kron sigma_j
```

All first-pass matrices are real symmetric, so they are compatible with a spin-singlet even-parity pairing test:

```text
Delta(k) = Delta^T(-k)
```

## 3. First Candidate Pairing Family

The first route-A candidate was:

```text
M0 = tau0 kron sigma0
M1 = taux kron sigma0
Delta_orb(eta) = Delta0 normalize[M0 + eta M1]
```

Interpretation:

1. `M0` is local identity-like s-wave pairing in the internal basis.
2. `M1` is layer-structured, same-sublattice interlayer pairing.
3. After projection, `M1` is expected to increase off-diagonal band-basis pairing weight.

This family is not a claim about the microscopic MATBG pairing glue. It is a controlled phenomenological probe used to test whether interband content can produce robust stiffness signatures.

## 3.1 Updated BM-Projection Candidate

After the first BM eigenvector projection test, the stronger working candidate is:

```text
M0 = tau0 kron sigma0
M1 = taux kron sigmax
Delta_orb(eta) = Delta0 normalize[M0 + eta M1]
```

Reason:

1. In a time-reversal-aligned proxy, `M0` projects to a band-diagonal baseline.
2. `taux kron sigmax` gives a larger projected off-diagonal weight than `taux kron sigma0`, `tau0 kron sigmaz`, or `tauz kron sigmaz`.
3. The effect becomes more visible for `n_keep = 4` and `n_keep = 6`, suggesting that the useful interband content primarily involves nearby remote bands rather than only the two central flat bands.

Important caveat:

The raw valley-plus / valley-minus BM eigenvectors require an explicit valley-basis sewing convention. Without that alignment, even `M0 = tau0 kron sigma0` projects to a highly off-diagonal matrix, so the off-diagonal diagnostic cannot yet be interpreted as physical interband pairing weight.

## 4. Normalization

Two scans are required:

1. `fixed_delta0`: keep the raw gap amplitude fixed.
2. `fixed_frobenius_norm`: rescale `M0 + eta M1` to keep the orbital Frobenius norm equal to that of `M0`.

The second scan is mandatory before claiming that a stiffness change is caused by pairing structure rather than by a larger gap norm.

## 5. Alternative M1 Matrices

If `taux kron sigmax` produces weak or ambiguous stiffness response, test:

```text
M1b = taux kron sigma0
M1c = tau0 kron sigmaz
M1d = tauz kron sigmaz
```

Use these only after recording why the first candidate was insufficient.

## 6. Gate 1 Acceptance

Before any stiffness scan, this pairing family must pass:

1. Hermitian BdG construction;
2. particle-hole paired-spectrum check between `k` and `-k`;
3. gauge-covariant projection check;
4. gauge-randomized BdG spectrum invariance;
5. monotonic or interpretable increase of BZ-averaged off-diagonal pairing weight with `eta`.

If any of these fail, do not run production scans.
