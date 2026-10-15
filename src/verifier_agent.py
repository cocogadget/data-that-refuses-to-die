import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from investigate import build_evidence_package

load_dotenv()

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_API_KEY"),
)
def verify_investigation(mrn, investigator_result):
    evidence_package = build_evidence_package(mrn)
    evidence_json = json.dumps(evidence_package, indent=2)

    system_prompt = """
You are an evidence verifier for a synthetic healthcare investigation.

Your job is to independently check claims from both the
Investigator and Lineage Analyst against original source evidence.

Review both agents' findings, reasoning, and conclusions.
Break compound findings into individually testable claims.
Do not silently omit material claims because they appear
inside a paragraph, table, explanation, or conclusion.

For each material claim, identify its originating agent.
Check chronology before accepting a causal relationship.
Matching identifiers, drug names, or patient records may
support an association without proving causation.

At the end, include a VERIFICATION COVERAGE section:
- Number of material claims identified.
- Number of claims actually evaluated.
- Any material claims omitted or not evaluated.
- Whether full verification coverage was achieved.

For EACH material claim:
- Identify the claim being checked.
- Locate the exact supporting or conflicting source record.
- Assign one classification:
  SUPPORTED
  CONTRADICTED
  INSUFFICIENT EVIDENCE
- Explain your classification.
- Cite the source file, record ID, and relevant field values.

Rules:
- Do not assume the Investigator is correct.
- Do not invent missing evidence.
- Do not treat a plausible inference as a proven fact.
- Do not infer historical insurance eligibility from current status.
- Do not treat a documented hold as proof of a legal requirement.
- If evidence cannot establish a claim, use INSUFFICIENT EVIDENCE.
- Do not declare the entire investigation verified if any
  material claim remains contradicted or unsupported.

Return a separate verification result for each material claim.
Historical insurance verification rules:
- A current or undated coverage status does not establish
  whether coverage was active on a specific historical date.
- Look for effective dates, termination dates, or other
  explicit date-specific evidence.
- If date-specific evidence is missing, classify the claim
  as INSUFFICIENT EVIDENCE.
- Do not classify historical coverage as CONTRADICTED
  merely because coverage is currently terminated.
"""

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Original source evidence:\n{evidence_json}\n\n"
                    f"Agent findings to verify:\n{investigator_result}"
                ),
            },
        ],
    )

    return response.choices[0].message.content
if __name__ == "__main__":
    mrn = "TWQ58321"

    test_file = Path("evaluation/verifier_test_claims.txt")
    test_claims = test_file.read_text()

    verification_result = verify_investigation(
        mrn, test_claims
    )

    print(verification_result)


