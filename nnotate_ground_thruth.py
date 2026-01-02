import csv
from pathlib import Path
from LOADERS.pdf_loader import load_pdf

RESUMES_DIR = Path("DATA/resumes")
JOBS_DIR = Path("DATA/jobs")
GT_FILE = Path("DATA/ground_truth.csv")

def main():
    with GT_FILE.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        if row["match"] != "-1":
            continue

        cv_text = load_pdf(RESUMES_DIR / row["cv_id"])
        job_text = load_pdf(JOBS_DIR / row["job_id"])

        print("\n" + "=" * 80)
        print("CV:", row["cv_id"])
        print(cv_text[:1200])
        print("\nJOB:", row["job_id"])
        print(job_text[:1200])
        print("=" * 80)

        label = input("Match? (1 = yes, 0 = no): ").strip()
        while label not in {"0", "1"}:
            label = input("Enter 1 or 0: ").strip()

        row["match"] = label

    with GT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cv_id", "job_id", "match"])
        writer.writeheader()
        writer.writerows(rows)

    print("Annotation complete.")

if __name__ == "__main__":
    main()


