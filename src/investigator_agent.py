import json
import os
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI

from investigate import build_evidence_package

load_dotenv()

api_key = os.getenv("NEBIUS_API_KEY")

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=api_key,
)

def investigate_patient(mrn):
    evidence_package = build_evidence_package(mrn)
    evidence_json = json.dumps(evidence_package, indent=2)
    system_prompt = """
You are an evidence-grounded investigator analyzing records from a simulated healthcare system.

Use only the evidence provided to you.

Your job is to:
- identify evidence that persists across sources
- identify inconsistencies or suspicious relationships
- distinguish facts from inferences
- explicitly state when evidence is insufficient
- cite the source file supporting each finding

Do not:
- invent missing facts
- assume facts based on general healthcare knowledge
- diagnose the patient
- treat an inference as a confirmed fact

For each finding, return:
FINDING:
EVIDENCE:
REASONING:
CONFIDENCE:
UNRESOLVED QUESTIONS:
"""
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"Analyze this evidence package:\n\n{evidence_json}",
            },

        ],
    )

    return response.choices[0].message.content

def save_investigation_run(mrn, result):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"evaluation/investigator_run_{mrn}_{timestamp}.txt"

    with open(filename, "w") as file:
        file.write(result)

 
if __name__ == "__main__":
    result = investigate_patient("TWQ58321")
    print(result)
    save_investigation_run("TWQ58321", result)
