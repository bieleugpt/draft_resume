
'''
import os
import csv

RESUMES_DIR = "DATA/resumes"
JOBS_DIR = "DATA/jobs"
OUTPUT_FILE = "DATA/ground_truth.csv"

def main():
    resumes = sorted([
        f.replace(".txt", "")
        for f in os.listdir(RESUMES_DIR)
        if f.endswith(".txt")
    ])

    jobs = sorted([
        f.replace(".txt", "")
        for f in os.listdir(JOBS_DIR)
        if f.endswith(".txt")
    ])

    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["cv_id", "job_id", "match"])

        for cv in resumes:
            for job in jobs:
                writer.writerow([cv, job, -1])

    print(f"Ground truth template created: {OUTPUT_FILE}")
    print(f"{len(resumes)} resumes × {len(jobs)} jobs")

if __name__ == "__main__":
    main()


'''







import csv
from dataset_utils import list_pdfs

RESUMES_DIR = "DATA/resumes"
JOBS_DIR = "DATA/jobs"
OUTPUT_FILE = "DATA/ground_truth.csv"

def main():
    resumes = list_pdfs(RESUMES_DIR)
    jobs = list_pdfs(JOBS_DIR)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["cv_id", "job_id", "match"])

        for cv in resumes:
            for job in jobs:
                writer.writerow([cv.name, job.name, -1])

    print(f"Ground truth created with {len(resumes)} CVs × {len(jobs)} jobs")

if __name__ == "__main__":
    main()
