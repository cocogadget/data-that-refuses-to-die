
import csv
import json
def find_records(filename, mrn):
	records = []
	with open(filename, newline="") as file:
		reader = csv.DictReader(file)
		for row in reader:
		    if row["mrn"] == mrn:
		        records.append(row)
	return records


target_mrn = "TWQ58321"

evidence_files = [
	"data/patient_demographics.csv",
	"data/patient_insurance.csv",
	"data/encounters.csv",
	"data/medications.csv",
	"data/historical_claims.csv",
	"data/holds.csv",
]

def build_evidence_package(mrn):
    evidence_package = {}

    for filename in evidence_files:
        records = find_records(filename, mrn)
        evidence_package[filename] = records

    return evidence_package


if __name__ == "__main__":
    evidence_package = build_evidence_package(target_mrn)
    print(json.dumps(evidence_package, indent=2))

