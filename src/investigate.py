
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

evidence_package = {}

for filename in evidence_files:
    records = find_records(filename, target_mrn)
    evidence_package [filename] = records

print(json.dumps(evidence_package, indent=2))

