# Investigator Baseline — Control Patient

## Run Information

- Target MRN: TWQ58321
- Model: NVIDIA Nemotron 3 Super 120B
- Purpose: First end-to-end Investigator evaluation

## Test Objective

Determine whether the Investigator can analyze a structured
six-source evidence package while remaining grounded in the
supplied evidence.


## Observed Strengths

- Identified MRN persistence across all six evidence sources.
- Correlated encounter and medication records.
- Connected historical insurance, medication, and claim evidence.
- Identified the active behavioral-health record hold.
- Cited source files supporting its findings.
- Distinguished facts from uncertainty.
- Lowered confidence when exact insurance effective dates were unavailable.

## Observed Failure

The Investigator stated that escitalopram was discontinued in
"September 2020."

However, the cited medication evidence states `2025-09-20`, and
the Investigator subsequently referred to September 2025 in the
same reasoning section.

This is a generated factual inconsistency that is contradicted by
the supplied evidence.

## Why This Matters

Evidence citation alone does not guarantee that generated
reasoning faithfully reproduces the cited evidence.

This failure becomes a test case for the planned independent
Verifier component.

## Future Verification Test

The Verifier should be able to:

1. Extract factual claims from Investigator findings.
2. Compare those claims against the cited source evidence.
3. Flag claims that contradict or lack support in the evidence.
4. Preserve supported findings while identifying generated errors.

## Raw Investigator Output
