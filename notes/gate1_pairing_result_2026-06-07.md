# Gate 1 Pairing Result

日期：2026-06-07  
命令：

```text
python3 scripts/run_pairing_definition_gate.py
```

## Pairing Family

First route-A family:

```text
M0 = tau0 kron sigma0
M1 = taux kron sigma0
Delta_orb(eta) = Delta0 normalize[M0 + eta M1]
```

The script tests both:

```text
fixed_frobenius_norm
fixed_delta0
```

## Result

The algebraic Gate 1 checks pass in the toy projected-basis setup:

1. `Delta(k) = Delta^T(-k)` passes at numerical precision.
2. BdG Hermiticity error is zero within numerical precision.
3. Paired-spectrum particle-hole check is at `~1e-16`.
4. Gauge-projection check is at `~1e-16`.
5. Gauge-randomized BdG spectrum is invariant at `~1e-16`.

The interband diagnostic behaves as intended in the time-reversal-like toy setup:

```text
eta = 0.00 -> W_inter = 0.000000
eta = 0.10 -> W_inter = 0.004181
eta = 0.25 -> W_inter = 0.025697
eta = 0.50 -> W_inter = 0.095947
eta = 0.75 -> W_inter = 0.193167
eta = 1.00 -> W_inter = 0.298385
```

## Interpretation

This does not yet prove that the pairing family produces a useful MATBG stiffness signature. It only verifies the algebraic contract:

```text
orbital pairing -> band projection -> gauge-covariant BdG object
```

The next check must use actual BM eigenvectors. If `eta` fails to tune off-diagonal weight after BM projection, try the backup matrices listed in `notes/pairing_matrix_choice.md`.

## Decision

Proceed with route A:

```text
Define pairing in orbital basis first, then project into band basis.
```

Do not use arbitrary constant band-basis off-diagonal pairing as a main-text mechanism.
