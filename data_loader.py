

#data_loader.py

from pathlib import Path
from LOADERS.pdf_loader import load_pdf

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "DATA"
RESUMES_DIR = DATA_DIR / "resumes"
JOBS_DIR = DATA_DIR / "jobs"


def load_resumes():
    resumes = {}
    for pdf in RESUMES_DIR.glob("*.pdf"):
        resumes[pdf.name] = load_pdf(pdf)
    return resumes


def load_jobs():
    jobs = {}
    for pdf in JOBS_DIR.glob("*.pdf"):
        jobs[pdf.name] = load_pdf(pdf)
    return jobs
