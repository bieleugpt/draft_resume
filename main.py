from ingestion import ingest_file
from structuring import structure_document
from embedding import embed_structured_document
from matching.scorer import compute_score
from explanation import explain_match

from pathlib import Path
import random
import numpy as np
import torch
from statistics import mean, stdev
import matplotlib.pyplot as plt

DEBUG = True
N_RUNS = 5

random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

EXPECTED_KEYS = [
    "hard_skills",
    "soft_skills",
    "tools_technologies",
    "domain_knowledge",
    "experience",
    "education",
    "full_text"
]


def single_run(cv_path, job_path):
    cv_text = ingest_file(cv_path)
    job_text = ingest_file(job_path)

    cv_structured = structure_document(cv_text, "cv")
    job_structured = structure_document(job_text, "job")

    for k in EXPECTED_KEYS:
        cv_structured.setdefault(k, "")
        job_structured.setdefault(k, "")

    cv_embeddings = embed_structured_document(cv_structured)
    job_embeddings = embed_structured_document(job_structured)

    for k in EXPECTED_KEYS:
        cv_embeddings.setdefault(k, None)
        job_embeddings.setdefault(k, None)

    scores = compute_score(cv_embeddings, job_embeddings)
    return scores, cv_structured, job_structured


def run_matching(cv_path, job_path, n_runs=5):
    all_scores = []
    last_cv = None
    last_job = None

    for i in range(n_runs):
        if DEBUG:
            print(f"\n######## RUN {i+1}/{n_runs} ########")

        scores, cv_s, job_s = single_run(cv_path, job_path)
        all_scores.append(scores)
        last_cv = cv_s
        last_job = job_s

        if DEBUG:
            print("Scores:", scores)

    aggregated = {}
    stability = {}

    all_keys = set().union(*[s.keys() for s in all_scores])

    for k in all_keys:
        values = [s[k] for s in all_scores if k in s]
        aggregated[k] = mean(values)
        stability[k] = stdev(values) if len(values) > 1 else 0.0

    explanation = explain_match(aggregated, last_cv, last_job)
    return aggregated, stability, explanation


'''
def plot_strengths(scores):
    labels = ["Forces", "Adéquation moyenne", "Faiblesses"]
    bins = [0, 0, 0]

    for v in scores.values():
        if v >= 0.6:
            bins[0] += 1
        elif v >= 0.4:
            bins[1] += 1
        else:
            bins[2] += 1

    plt.pie(bins, labels=labels, autopct="%1.0f%%", startangle=90)
    plt.title("Analyse Forces / Faiblesses du CV")
    plt.axis("equal")
    plt.show()


if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent

    scores_mean, scores_std, explanation = run_matching(
        BASE_DIR / "DATA" / "CV.pdf",
        BASE_DIR / "DATA" / "offre.txt",
        n_runs=N_RUNS
    )

    print("\n==============================")
    print("MATCHING FINAL")
    print("==============================")
    for k, v in scores_mean.items():
        print(f"{k}: {v:.3f} ± {scores_std[k]:.3f}")

    print("\nAI Explanation:")
    print(explanation)

    plot_strengths(scores_mean)

    '''


def plot_strengths(scores_mean):
    categories = {
        "Hard skills": scores_mean.get("hard_skills", 0),
        "Soft skills": scores_mean.get("soft_skills", 0),
        "Domain knowledge": scores_mean.get("domain_knowledge", 0),
        "Tools / Tech": scores_mean.get("tools_technologies", 0),
        "Experience": scores_mean.get("experience", 0),
        "Education": scores_mean.get("education", 0),
    }

    strength = medium = weakness = 0

    for score in categories.values():
        if score >= 0.6:
            strength += 1
        elif score >= 0.4:
            medium += 1
        else:
            weakness += 1

    labels = ["Forces", "Adéquation moyenne", "Faiblesses"]
    values = [strength, medium, weakness]
    colors = ["#2ecc71", "#f1c40f", "#e74c3c"]

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        values,
        labels=labels,
        autopct="%1.0f%%",
        startangle=90,
        colors=colors
    )
    ax.set_title("Analyse Forces / Faiblesses du CV")
    ax.axis("equal")

    return fig

if __name__ == "__main__":
    from pathlib import Path

    BASE_DIR = Path(__file__).parent
    cv_path = BASE_DIR / "DATA" / "CV.pdf"
    job_path = BASE_DIR / "DATA" / "offre.txt"

    scores_mean, scores_std, explanation = run_matching(
        cv_path=cv_path,
        job_path=job_path,
        n_runs=5
    )

    print("SCORES MOYENS :", scores_mean)
    print("ECART-TYPE :", scores_std)
    print("EXPLICATION :", explanation)