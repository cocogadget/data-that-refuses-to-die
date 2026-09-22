
import csv
def find_records(filename, mrn):
	records = []
	with open(filename, newline="") as file:
		reader = csv.DictReader(file)
		for row in reader:
		    if row["mrn"] == mrn:
		        records.append(row)
	return records


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
    records = find_records(filename, "TWQ58321")
    evidence_package [filename] = records

print(evidence_package)

