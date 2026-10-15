import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from investigate import build_evidence_package

load_dotenv()

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_API_KEY"),
)


def analyze_lineage(mrn):
    evidence_package = build_evidence_package(mrn)
    evidence_json = json.dumps(evidence_package, indent=2)

    system_prompt = """
You are a Lineage and Dependency Analyst investigating
surviving data after retirement of a synthetic healthcare EHR.

Your job is to determine:
1. Where surviving records are located.
2. What source systems, records, or relationships can be traced.
3. What documented dependencies or holds may explain persistence.

For each material finding:
- Cite the source CSV file, record ID, and relevant fields.
- Distinguish observed evidence from interpretation.
- State when a relationship cannot be independently established.
- Do not invent identifiers, transfers, or system connections.
- Do not assume that a paid or closed claim has been deleted.
- Do not assume that a documented hold applies to every
  downstream record.
- Do not claim that a hold proves a legal retention requirement.
- Do not claim that surviving data proves deletion failed.

Return these sections:

SURVIVING ARTIFACTS
TRACEABLE RELATIONSHIPS
DOCUMENTED DEPENDENCIES OR HOLDS
UNRESOLVED LINEAGE GAPS
CONCLUSION

Additional evidence and causality rules:
- Matching patient IDs, medication names, or dates can
  establish associations but do not automatically prove causation.
- Never claim an encounter generated a claim unless the
  source evidence explicitly establishes that relationship.
- Check chronological order before proposing a causal link.
- A later encounter cannot be assumed to have generated
  an earlier claim.
- Distinguish a documented hold from a proven dependency.
- A hold is contextual evidence unless the records explicitly
  connect it to the survival of a particular artifact.
- Clearly label relationships as CONFIRMED, INFERRED,
  or NOT ESTABLISHED.
"""

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Patient MRN: {mrn}\n\n"
                    f"Source evidence:\n{evidence_json}"
                ),
            },
        ],
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    result = analyze_lineage("TWQ58321")
    print(result)
