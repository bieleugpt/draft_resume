import csv
from collections import defaultdict

GT_FILE = "DATA/ground_truth.csv"

def main():
    cv_counts = defaultdict(int)
    job_counts = defaultdict(int)
    total = 0
    positives = 0

    with open(GT_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            if row["match"] == "1":
                positives += 1
                cv_counts[row["cv_id"]] += 1
                job_counts[row["job_id"]] += 1

    print("Total pairs:", total)
    print("Positive matches:", positives)
    print("Positive ratio:", positives / total if total else 0)

    print("\nMatches per CV:")
    for cv, count in cv_counts.items():
        print(f"{cv}: {count}")

    print("\nMatches per Job:")
    for job, count in job_counts.items():
        print(f"{job}: {count}")

if __name__ == "__main__":
    main()
