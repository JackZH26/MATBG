# PRB Readiness Audit

Date: 2026-06-10

Manuscript:
`Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex`

Review source:
`/Users/jackzhou/Downloads/PRB_Review_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_MATBG_2026-06-10.md`

## Current Status

The active manuscript is now a local PRB major-revision response checkpoint.
It includes the revised main manuscript, revised Supplemental Material, cover
letter, point-by-point response to the referee report, new major-revision data
products, reproducibility scripts, and a validation/package audit chain.

The final observable policy for the current mechanism-paper scope remains
unchanged in one important respect: normalized response ratios are the
claim-bearing quantities, while raw finite-band response values and converted
absolute units are diagnostic or provenance quantities only.  The revision
strengthens the evidence behind the normalized diagnostic; it does not convert
the paper into an absolute-stiffness or device-calibrated experimental
comparison.

## Review-Driven Requirements

| Requirement from review | Current evidence | Status |
|---|---|---|
| Broaden beyond one working pairing ansatz | `data/processed/pairing_family_response_summary.csv`, `figures/pairing_family_response_summary.pdf`, `scripts/audit_pairing_family_response.py` | Satisfied for the declared eight-direction orbital-pairing family |
| Add stronger grid/truncation/shell robustness | `data/processed/prb_major_revision_robustness_summary.csv`, `figures/prb_major_revision_robustness_matrix.pdf`, `scripts/audit_prb_major_revision_robustness.py` | Satisfied for production/expanded truncations, with low-truncation boundary disclosed |
| Quantify valley-sewing sensitivity | `data/processed/valley_sewing_response_sensitivity_summary.csv`, `figures/valley_sewing_response_sensitivity.pdf`, `scripts/audit_valley_sewing_response_sensitivity.py` | Satisfied for the current diagnostic; not a valley-basis-independent claim |
| Clarify normalized versus absolute observables | main text, Supplemental Material, `scripts/audit_observable_policy.py` | Satisfied for normalized finite-band diagnostic scope |
| Improve reproducibility and data availability | GitHub repository statement, manifest, package builder, validation chain | Satisfied for local package checkpoint |
| Write a point-by-point response | `submission/Zhou_PRB_Response_To_Reviewers_2026.md` | Satisfied as a draft response package artifact |

## Major-Revision Evidence Summary

Pairing-family response:

```text
fixed-Frobenius: 32/32 positive, +6.43% to +9.49%
fixed-Delta0:    -1.46% to +2.91%
audit:           7/7 checks pass
```

Grid/truncation/shell robustness:

```text
all fixed-Frobenius rows:       172/180 positive
n_keep >= 6:                    120/120 positive, +1.07% to +13.60%
n_keep >= 6 and N_shell >= 3:    80/80 positive, +4.37% to +13.60%
disclosed boundary:             n_keep=4, mu=-4 meV
audit:                          12/12 checks pass
```

Valley-partner response sensitivity:

```text
tr_sewn: 24/24 positive, +4.37% to +13.60%, PH error 0
alternatives: sign-sensitive and PH-error sensitive stress tests
audit: 8/8 checks pass
```

## Remaining Boundaries

The revised paper still does not claim:

1. continuum-limit numerical stiffness values,
2. valley-basis-independent absolute stiffness,
3. direct quantitative agreement with experimental stiffness,
4. calibrated device-level carrier-density or superconducting-dome matching,
5. universality across all possible pairing channels.

These boundaries are not defects in the present scope; they define the current
mechanism-paper claim.  The manuscript now contains enough evidence to answer
the first-round referee's major concerns without changing into a broader
experimental-comparison paper.

## Current Validation Gates

Required before treating the package as current:

```bash
python3 scripts/run_prb_validation.py
python3 scripts/build_prb_submission_package.py
python3 scripts/audit_prb_submission_checkpoint.py
```

The validation chain must include the three new major-revision audits:

```text
pairing_family_response_audit
major_revision_robustness_audit
valley_response_sensitivity_audit
```

## Readiness Judgment

Current level: local PRB major-revision response checkpoint for the normalized
finite-band mechanism-paper scope.

The paper is stronger than the 2026-06-09 checkpoint because the claim no
longer rests only on one pairing direction, one modest grid, one retained-band
truncation, or an unaudited valley-sewing convention.  The remaining task
before actual journal upload is user approval and, if the upload is delayed, a
fresh literature sweep immediately before submission.
