# PRB Major-Revision Robustness Audit

Date: 2026-06-10

## Purpose

This note records the first grid/truncation/shell robustness matrix requested
by the PRB-style review.  It addresses the concern that the normalized response
signature was previously supported mainly by the dense `nk=7`, `n_keep=6`,
`n_shell=3` calculation plus selected higher-grid checks.

## Commands

```bash
python3 scripts/run_prb_major_revision_robustness.py
python3 scripts/audit_prb_major_revision_robustness.py
python3 scripts/plot_prb_major_revision_robustness.py
```

## Scope

The current matrix uses the original working direction `M1=taux_sigmax` and
the `tr_sewn` valley convention:

```text
nk       = 9, 11, 13, 15
n_keep   = 4, 6, 8
n_shell  = 2, 3, 4
mu       = -4, -2, 0, 2, 4 meV
eta      = 0, 0.5, 1
normalizations = fixed_frobenius_norm, fixed_delta0
```

## Outputs

```text
data/processed/prb_major_revision_robustness_matrix.csv
data/processed/prb_major_revision_robustness_summary.csv
data/processed/prb_major_revision_robustness_audit.csv
figures/prb_major_revision_robustness_matrix.png
figures/prb_major_revision_robustness_matrix.pdf
```

The raw matrix contains `1080` rows.  The eta=1 versus eta=0 summary contains
`360` rows.

## Main Result

The full fixed-Frobenius matrix is not globally all-positive:

```text
fixed_frobenius all rows: 172/180 positive
range: -42.222% to +16.604%
```

All eight nonpositive fixed-Frobenius rows are confined to the lowest retained
band truncation, `n_keep=4`, at the hole-side endpoint `mu=-4 meV`:

```text
n_shell=3, n_keep=4, mu=-4 meV: -10.095% to -0.891%
n_shell=4, n_keep=4, mu=-4 meV: -42.222% to -41.233%
```

For the production and expanded retained-band truncations, the sign is stable:

```text
n_keep >= 6: 120/120 positive
range: +1.071% to +13.603%

n_keep >= 6 and n_shell >= 3: 80/80 positive
range: +4.374% to +13.603%
mean:  +8.268%
```

The fixed-Delta0 control remains weak and sign-sensitive over the full matrix:

```text
fixed_delta0 all rows: 113/180 positive
range: -4.624% to +3.301%
mean:  +0.286%
```

## Audit Status

The machine-readable audit passes all current scoped checks:

```text
data/processed/prb_major_revision_robustness_audit.csv
```

It does not certify a global all-truncation positive response.  Instead, it
certifies that:

1. the planned `nk`, `n_keep`, `n_shell`, `mu`, and `eta` axes are present;
2. all fixed-Frobenius responses are positive for `n_keep>=6`;
3. the production-scope minimum response exceeds four percent for
   `n_keep>=6` and `n_shell>=3`;
4. all nonpositive rows are confined to `n_keep=4` at `mu=-4 meV`;
5. the fixed-Delta0 control remains sign-sensitive;
6. particle-hole spectrum errors remain below the audit tolerance.

## Manuscript Implication

The revised manuscript can now make a stronger, but still scoped, numerical
statement:

```text
The fixed-Frobenius normalized response remains positive throughout the tested
production and expanded retained-band truncations (`n_keep=6,8`) across
`nk=9,11,13,15`, `n_shell=2,3,4`, and `mu=-4,-2,0,2,4 meV`.
```

It should also explicitly disclose the low-truncation boundary:

```text
At `n_keep=4`, the hole-side endpoint `mu=-4 meV` can become negative for
larger shell cutoffs, so the response is not globally independent of retained
band truncation.
```

This boundary is scientifically useful: it prevents the revised manuscript
from overclaiming and directly answers the reviewer's concern about truncation
sensitivity.
