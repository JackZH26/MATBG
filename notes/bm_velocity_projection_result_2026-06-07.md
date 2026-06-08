# BM Velocity Projection Gate Result

日期：2026-06-07

## Question

Can the BM normal-state velocity operator be projected into the retained band subspace and split cleanly into intra-band and inter-band parts?

## Command

```text
python3 scripts/run_bm_velocity_projection_gate.py --n-shell 3 --nk 3 --n-keep-values 2 4 6
```

## Result

The projected velocity matrices pass the basic numerical checks:

1. Hermiticity error is at `~1e-15`.
2. Intra/inter decomposition closes exactly within numerical precision.
3. Off-diagonal velocity weight is large, especially when remote bands are retained.

Summary:

```text
n_keep = 2, vx offdiag weight = 0.554661
n_keep = 2, vy offdiag weight = 0.464019
n_keep = 4, vx offdiag weight = 0.784512
n_keep = 4, vy offdiag weight = 0.750640
n_keep = 6, vx offdiag weight = 0.749013
n_keep = 6, vy offdiag weight = 0.835628
```

## Interpretation

The off-diagonal part of the band-basis velocity is substantial. This is the normal-state ingredient that will feed the geometric/interband-current sector in the later superfluid stiffness calculation.

This result does not yet compute `Dconv`, `Dgeom`, or `Dcross`; it only validates the normal-state velocity projection and matrix split required by that calculation.

## Decision

Proceed to the minimal BdG response engine only after keeping these conventions fixed:

```text
pairing partner convention: tr_sewn
pairing family: M0=tau0_sigma0, M1=taux_sigmax
velocity split: diagonal band velocity vs off-diagonal band velocity
```
