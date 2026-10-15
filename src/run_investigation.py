from datetime import datetime
from pathlib import Path

from investigator_agent import investigate_patient
from lineage_agent import analyze_lineage
from verifier_agent import verify_investigation


def run_investigation(mrn):
    print("STEP 1: Running Investigator...", flush=True)
    investigator_result = investigate_patient(mrn)

    print("STEP 2: Running Lineage Analyst...", flush=True)
    lineage_result = analyze_lineage(mrn)

    print("STEP 3: Running Verifier...", flush=True)

    combined_findings = (
        "INVESTIGATOR FINDINGS:\n"
        + investigator_result
        + "\n\nLINEAGE FINDINGS:\n"
        + lineage_result
    )

    verifier_result = verify_investigation(mrn, combined_findings)

    report = (
        f"PATIENT MRN: {mrn}\n\n"
        f"=== INVESTIGATOR ===\n{investigator_result}\n\n"
        f"=== LINEAGE ANALYST ===\n{lineage_result}\n\n"
        f"=== VERIFIER ===\n{verifier_result}\n"
    )

    return report


if __name__ == "__main__":
    mrn = "TWQ58321"

    report = run_investigation(mrn)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path(
        f"evaluation/full_investigation_{mrn}_{timestamp}.txt"
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(report)

    print(f"\nInvestigation saved to: {output_file}")
