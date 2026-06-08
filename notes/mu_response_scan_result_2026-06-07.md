# First Mu Response Scan Result

日期：2026-06-07

## Question

Does the eta-dependent response persist away from charge neutrality?

## Command

```text
python3 scripts/run_mu_response_scan.py --n-shell 3 --nk 7 --n-keep 6 --output data/processed/mu_response_scan_nk7_nkeep6.csv
python3 scripts/plot_mu_response_scan.py --input data/processed/mu_response_scan_nk7_nkeep6.csv --output figures/mu_response_scan_nk7_nkeep6.png
```

## Setup

```text
n_shell = 3
nk = 7
n_keep = 6
mu = -6, -4, -2, 0, 2, 4, 6 meV
eta = 0, 0.5, 1
Delta0 = 1 meV
partner = tr_sewn
M0 = tau0_sigma0
M1 = taux_sigmax
```

## Main Result

Define:

```text
D_iso = (Dxx_total + Dyy_total) / 2
```

For `eta=1` relative to `eta=0`, the fixed-Frobenius scan gives:

```text
mu = -6 meV -> +11.50%
mu = -4 meV ->  +8.91%
mu = -2 meV ->  +5.37%
mu =  0 meV ->  +8.17%
mu =  2 meV ->  +9.49%
mu =  4 meV ->  +6.62%
mu =  6 meV ->  +5.75%
```

For fixed raw `Delta0`, the same comparison is much weaker:

```text
mu = -6 meV ->  +3.62%
mu = -4 meV ->  +2.91%
mu = -2 meV ->  -1.10%
mu =  0 meV ->  +1.12%
mu =  2 meV ->  +1.19%
mu =  4 meV ->  -0.05%
mu =  6 meV ->  -0.09%
```

## Interpretation

The first mu scan supports two working conclusions:

1. The eta-dependent response is not confined to charge neutrality.
2. The size and even sign of the response depends strongly on normalization convention.

This means the project should avoid a simple statement like:

```text
interband pairing always enhances stiffness
```

The safer statement is:

```text
In this finite-band BM response gate, the orbital-projected interband-pairing direction produces a smooth eta-dependent response, but the magnitude of the enhancement is strongly conditioned on how the gap norm is held fixed.
```

## Observable Status

Current support level:

```text
D_iso trend: promising but still gate-level
geometric fraction trend: useful as explanation
anisotropy: not yet robust enough for a primary signature
doping dependence: promising enough to justify denser scan
```

## Next Step

Run a more focused scan around the response maximum:

```text
mu = -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5 meV
eta = 0, 0.25, 0.5, 0.75, 1
nk = 7 first, then nk = 9 for confirmation
```

Before presenting final figures, add a conversion layer for:

```text
raw response -> normalized response -> physical units
```

and decide which normalization convention belongs in the main text.
