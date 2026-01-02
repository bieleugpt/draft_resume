'''
import csv
from pathlib import Path

RESUMES_DIR = Path("DATA/resumes")
JOBS_DIR = Path("DATA/jobs")
GT_FILE = Path("DATA/ground_truth.csv")

def load_text(path):
    return path.read_text(encoding="utf-8")

def main():
    rows = []

    with GT_FILE.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        if row["match"] != "-1":
            continue

        cv_text = load_text(RESUMES_DIR / f"{row['cv_id']}.txt")
        job_text = load_text(JOBS_DIR / f"{row['job_id']}.txt")

        print("\n" + "=" * 80)
        print(f"CV: {row['cv_id']}")
        print(cv_text[:800])
        print("\nJOB:", row["job_id"])
        print(job_text[:800])
        print("=" * 80)

        label = input("Match? (1 = yes, 0 = no): ").strip()
        while label not in {"0", "1"}:
            label = input("Please enter 1 or 0: ").strip()

        row["match"] = label

    with GT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cv_id", "job_id", "match"])
        writer.writeheader()
        writer.writerows(rows)

    print("Ground truth updated.")

if __name__ == "__main__":
    main()
'''




'''

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

        cv_path = RESUMES_DIR / row["cv_id"]
        job_path = JOBS_DIR / row["job_id"]

        if not cv_path.exists():
            raise FileNotFoundError(f"CV not found: {cv_path}")
        if not job_path.exists():
            raise FileNotFoundError(f"Job not found: {job_path}")

        cv_text = load_pdf(str(cv_path))
        job_text = load_pdf(str(job_path))

        print("\n" + "=" * 100)
        print("CV:", row["cv_id"])
        print(cv_text[:1200])

        print("\nJOB:", row["job_id"])
        print(job_text[:1200])
        print("=" * 100)

        label = input("Match? (1 = yes, 0 = no): ").strip()
        while label not in {"0", "1"}:
            label = input("Please enter 1 or 0: ").strip()

        row["match"] = label

    with GT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cv_id", "job_id", "match"])
        writer.writeheader()
        writer.writerows(rows)

    print("✅ Ground truth annotation completed successfully.")


if __name__ == "__main__":
    main()
'''














import csv
from pathlib import Path
from LOADERS.pdf_loader import load_pdf

RESUMES_DIR = Path("DATA/resumes")
JOBS_DIR = Path("DATA/jobs")
GT_FILE = Path("DATA/ground_truth.csv")


def save(rows):
    with GT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cv_id", "job_id", "match"])
        writer.writeheader()
        writer.writerows(rows)


def main():
    with GT_FILE.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for i, row in enumerate(rows):
        if row["match"] != "-1":
            continue

        cv_path = RESUMES_DIR / row["cv_id"]
        job_path = JOBS_DIR / row["job_id"]

        cv_text = load_pdf(str(cv_path))
        job_text = load_pdf(str(job_path))

        print("\n" + "=" * 100)
        print(f"[{i+1}/{len(rows)}]")
        print("CV:", row["cv_id"])
        print(cv_text[:1000])

        print("\nJOB:", row["job_id"])
        print(job_text[:1000])
        print("=" * 100)

        label = input("Match? (1 = yes, 0 = no): ").strip()
        while label not in {"0", "1"}:
            label = input("Please enter 1 or 0: ").strip()

        row["match"] = label
        save(rows)  # 🔥 SAUVEGARDE IMMÉDIATE

        print("✔ Saved")

    print("✅ Annotation finished")


if __name__ == "__main__":
    main()



