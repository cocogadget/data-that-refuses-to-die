# The Data That Refuses to Die

**An evidence-grounded, three-agent AI investigation of data surviving a legacy healthcare system retirement.**

Built by **CocoaGadget Labs** for the **Nebius × NVIDIA Global AI Hackathon — Best Apps & Agents track**.

## The Problem

Retiring a healthcare system does not necessarily mean every copy of its data disappears.

Historical claims, medication records, insurance information, and other artifacts may remain in downstream systems after the original application has been retired.

That creates a difficult question:

**Did the data actually disappear, or did it survive somewhere else?**

Finding a surviving record is only the beginning. An investigation must also distinguish what the evidence proves from what it merely suggests.

## What This Project Does

The Data That Refuses to Die uses three AI agents to investigate synthetic healthcare records and assess whether historical information remains observable across a simulated system-retirement environment.

The investigation focuses on three questions:

1. Did the data actually disappear?
2. Where did surviving data go, and why did it survive?
3. Can an AI-assisted investigation produce a conclusion that can be independently checked against source evidence?

The application uses structured CSV records as its evidence source. AI-generated conclusions are evaluated against those records rather than accepted as evidence by themselves.

## Three-Agent Architecture

### 1. Investigator

Examines records associated with a patient identifier and identifies potentially surviving information, inconsistencies, and unanswered questions.

### 2. Lineage and Dependency Analyst

Examines relationships among records, downstream locations, documented holds, and possible dependencies.

It must distinguish confirmed relationships from inferences and avoid assuming that records sharing a patient or medication necessarily share a causal origin.

### 3. Assurance and Verification Agent

Reviews the findings of both preceding agents against the original evidence package.

Material claims are assessed using three classifications:

- **SUPPORTED:** The supplied evidence supports the claim.
- **CONTRADICTED:** The supplied evidence conflicts with the claim.
- **INSUFFICIENT EVIDENCE:** The supplied evidence cannot establish the claim.

The verifier is an additional AI-based assurance layer, not an independent proof engine. Its conclusions remain subject to review against the underlying records.

## Technology

- Python 3.9
- Nebius Token Factory API
- NVIDIA Nemotron model: `nvidia/nemotron-3-super-120b-a12b`
- OpenAI-compatible Python API client
- Python dotenv
- CSV-based synthetic evidence
- Local text-based investigation reports

The `openai` Python package is used as an API client configured for the Nebius endpoint. The application does not require an OpenAI model.

## Synthetic Healthcare Evidence

The project contains synthetic records across six datasets:

| Dataset | Purpose |
|---|---|
| `patient_demographics.csv` | Patient identifiers and demographic context |
| `patient_insurance.csv` | Insurance coverage records |
| `encounters.csv` | Clinical encounter history |
| `medications.csv` | Medication history and status |
| `historical_claims.csv` | Historical claims and surviving artifacts |
| `holds.csv` | Documented hold information |

The scenario models a retiring behavioral health EHR, an enterprise data lake/revenue-cycle environment, and ancillary clinical systems.

**All patient information is synthetic. No real patient health information is required.**

## Example Investigation: Patient 15

The primary end-to-end test case uses synthetic patient identifier `TWQ58321`.

The evidence includes:

- A historical Escitalopram claim dated March 20, 2025, recorded as surviving in the enterprise revenue-cycle environment.
- A later clinical encounter dated September 20, 2025, associated with a medication change.
- Historical insurance records with terminated coverage statuses but without sufficient effective-date information to establish coverage on every historical date.
- An active behavioral-health records hold whose existence is documented, but whose causal relationship to the surviving claim is not established.

This case tests whether agents can identify a surviving artifact without inventing relationships between records.

For example, the September 2025 encounter cannot be established as the origin of a claim dated March 2025 merely because the records refer to the same medication.

Likewise, a visible hold does not independently establish why a specific claim survived.

## Running the Project

### Prerequisites

- Python 3.9 or a compatible environment
- A Nebius Token Factory API key
- Internet access for model requests

### 1. Clone the repository

```bash
git clone https://github.com/cocogadget/data-that-refuses-to-die.git
cd data-that-refuses-to-die
```

### 2. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 3. Configure the API key

Create a `.env` file in the repository root containing:

```dotenv
NEBIUS_API_KEY=your_api_key_here
```

Do not commit your `.env` file or publish an API key.

### 4. Run the investigation

From the repository root:

```bash
python3 src/run_investigation.py
```

The current demonstration pipeline runs the investigation for synthetic patient `TWQ58321`.

It executes the Investigator, Lineage Analyst, and Verifier in sequence.

### 5. Review the report

A timestamped text report is saved under `evaluation/` using a filename similar to:

```text
full_investigation_TWQ58321_YYYYMMDD_HHMMSS.txt
```

The report contains the three agents' findings and verification results.

## Evaluation and Observed Failures

The project retains baseline outputs, controlled test claims, revised prompts, and retest artifacts in the `evaluation/` directory.

Two important failures informed the design:

**Historical coverage inference:** An early verifier incorrectly treated a currently terminated insurance record as proof that coverage was inactive on an earlier historical date. The revised verifier correctly classified the historical eligibility question as **INSUFFICIENT EVIDENCE** when effective and termination dates were unavailable.

**Chronology and causation:** An early lineage analysis suggested a later encounter generated an earlier claim and treated a documented hold as a causal dependency. The revised analysis improved temporal reasoning and separated documented context from established causation.

In a controlled three-claim verifier retest, the revised verifier correctly distinguished one supported claim, one contradicted claim, and one claim with insufficient evidence.

An integrated retest reported coverage of 24 material claims across the Investigator and Lineage Analyst outputs. That count is the verifier's own assessment, not independently validated proof of complete coverage or correctness.

One remaining limitation is imprecise wording about matching dates across related records, even when the underlying claim and encounter dates differ.

**The evaluation preserves these failures because the purpose is to investigate AI reliability, not conceal its weaknesses.**

## Current Limitations

- The application uses synthetic data, not live healthcare integrations.
- The current end-to-end demonstration is a command-line pipeline focused on one patient.
- Records are retrieved using an exact patient identifier.
- The agents can still make unsupported or imprecise statements.
- Verification uses an AI model and does not guarantee factual correctness.
- A documented retention hold is not automatically evidence of a legal requirement or a specific survival cause.
- A surviving artifact does not, by itself, prove that a deletion obligation was violated.
- The application is a prototype and is not intended for clinical decision-making or production compliance determinations.

## Design Principle

**AI may investigate, reason, and propose explanations. It cannot manufacture evidence.**

A trustworthy investigation must preserve the difference between what is observed, what is inferred, and what remains unknown.

## Repository

https://github.com/cocogadget/data-that-refuses-to-die

**CocoaGadget Labs — Investigate the evidence. Question the inference. Preserve the uncertainty.**
