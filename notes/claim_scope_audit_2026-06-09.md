# Claim Scope Audit

Date: 2026-06-09

Purpose:
lock the current PRB draft to a mechanism-paper claim scope.  The manuscript is
now strong enough to claim a reproducible normalized response signature, but it
should not imply final absolute stiffness, device-level filling calibration, or
a strict continuum limit.

Command:

```bash
python3 scripts/audit_claim_scope.py
```

Output:

```text
data/processed/claim_scope_audit.csv
```

Allowed main-paper claims:

```text
orbital-projected tr_sewn pairing construction
finite interband pairing weight W_inter ~= 0.108
fixed-Frobenius dense response enhancement over mu=-5...5 meV
selected-grid and nk=15 representative stability of the sign/scale
convergence-sufficiency support for the selected-grid mechanism claim
fixed-Delta0 as a weak/sign-sensitive control
central-flat-band filling crosswalk as a counting reference
```

Deferred claims:

```text
unconditional physical stiffness enhancement
direct experimental stiffness agreement
device-level carrier-density calibration
strict continuum-limit numerical values
microscopic identification of the pairing glue
valley-asymmetric or finite-momentum superconducting order
```

Result:

The audit script checks that the main text and Supplemental Material retain the
key conservative boundary phrases and do not contain a short list of forbidden
overclaims.  This is a text-level guardrail; it complements, but does not
replace, the numerical table verifier.

Current outcome:

```text
Claim-scope checks passed: 16/16
```
