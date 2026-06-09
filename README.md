# MATBG Research Workspace

This repository contains the working materials for a MATBG superfluid stiffness project centered on interband pairing, quantum geometry, and observable stiffness signatures.

## Current Core Files

1. `MATBG_Interband_Pairing_Superfluid_Stiffness_PhD_Proposal_2026_V2.md`  
   The proposal-level research plan.

2. `MATBG_Executable_Research_Plan_2026.md`  
   The operational research plan with work packages, acceptance criteria, and sprint tasks.

3. `MATBG_superfluid_weight_PRB_v2.tex`  
   Historical PRB-style baseline draft on band-basis decomposition of superfluid weight.

4. `Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex`
   Current PRB-targeted mechanism manuscript.

5. `Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_Supplemental_Material_2026.tex`
   Current Supplemental Material draft.

6. `notes/interband_pairing_definition.md`
   Working definition and validation requirements for interband pairing.

## Current Manuscript Status

The current PRB-targeted manuscript is a normalized-response mechanism paper.
Its central claim is that an orbital-projected interband-pairing direction
produces a reproducible, normalization-conditioned finite-band response
signature in MATBG. The current draft is a strong internal checkpoint, not yet
a final submission package.

The manuscript deliberately does not claim direct quantitative agreement with
experimental stiffness, a final absolute stiffness convention, a device-level
carrier-density calibration, or a continuum-limit extrapolation.

## Validation

Run the standard validation chain before manuscript-facing commits:

```bash
python3 scripts/run_prb_validation.py
```

The command writes:

```text
data/processed/prb_validation_summary.csv
```

It checks script syntax, claim-scope guardrails, observable policy, filling and
convergence sufficiency, manuscript/Supplemental Material table values,
submission-package mechanics, main/Supplemental Material LaTeX builds, and
blocking LaTeX log warnings.

## Research Owner

Jian Zhou  
Principal Investigator  
JZ Institute of Science, Hong Kong, China  
jack@jzis.org
