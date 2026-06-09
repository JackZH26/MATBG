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

7. `submission/Zhou_PRB_Cover_Letter_2026.md`
   Current Physical Review B cover letter draft.

## Current Manuscript Status

The current PRB-targeted manuscript is a normalized-response mechanism paper.
Its central claim is that an orbital-projected interband-pairing direction
produces a reproducible, normalization-conditioned finite-band response
signature in MATBG. The current repository state is a local PRB
submission-facing checkpoint for this mechanism-paper scope.

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
data/processed/prb_submission_manifest.csv
```

It checks script syntax, claim-scope guardrails, observable policy, filling and
convergence sufficiency, manuscript/Supplemental Material table values,
submission-package mechanics, submission-manifest completeness, main/Supplemental
Material LaTeX builds, cover letter presence/signature, and blocking LaTeX log
warnings.

## Local PRB Package Checkpoint

Build the local manuscript checkpoint package with:

```bash
python3 scripts/build_prb_submission_package.py
```

The command writes an ignored local package and zip under `submission/build/`
and records the tracked build summary in:

```text
data/processed/prb_submission_package_build.csv
```

The package is for local review and final-preparation work. It is not an APS
Editorial Manager upload; actual journal submission still requires user
approval and upload through the journal system.

Run the final local checkpoint audit after validation and package construction:

```bash
python3 scripts/audit_prb_submission_checkpoint.py
```

The command writes:

```text
data/processed/prb_submission_checkpoint_audit.csv
```

This audit checks cross-file consistency among the manuscript, Supplemental
Material, cover letter, README, manifest, validation summary, and ignored local
package outputs, including SHA-256 content matches for manifest-tracked files
inside both the package directory and zip archive.

The goal-level completion audit is recorded in:

```text
data/processed/prb_goal_completion_audit.csv
notes/prb_goal_completion_audit_2026-06-09.md
```

## Research Owner

Jian Zhou  
Principal Investigator  
JZ Institute of Science, Hong Kong, China  
jack@jzis.org
