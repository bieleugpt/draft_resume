# main.py

from ingestion import ingest_file
from structuring import structure_document
from embedding import embed_structured_document
from matching.scorer import compute_score
from matching.matching_pipeline import fuse_scores
from explanation import explain_match

from pathlib import Path
import random
import numpy as np
import torch
from statistics import mean, stdev

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
DEBUG = True

# -------------------------------------------------
# Reproductibilité contrôlée
# -------------------------------------------------
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

# -------------------------------------------------
# DEBUG UTIL
# -------------------------------------------------
def debug_print(title: str, data: dict):
    if not DEBUG:
        return

    print("\n" + "=" * 60)
    print(f"[DEBUG] {title}")
    print("=" * 60)

    for k, v in data.items():
        if k in ["raw_text", "full_text"]:
            continue
        print(f"- {k}:")
        print(v if v else "[EMPTY]")

# -------------------------------------------------
# SINGLE RUN
# -------------------------------------------------
def single_run(cv_path, job_path):
    # 1️⃣ Ingestion
    cv_text = ingest_file(cv_path)
    job_text = ingest_file(job_path)

    if DEBUG:
        print("\n[DEBUG] Ingestion OK")

    # 2️⃣ Structuration
    cv_structured = structure_document(cv_text, doc_type="cv")
    job_structured = structure_document(job_text, doc_type="job")

    debug_print("STRUCTURED CV", cv_structured)
    debug_print("STRUCTURED JOB", job_structured)

    # 3️⃣ Embeddings STRUCTURED
    cv_emb_struct = embed_structured_document(cv_structured)
    job_emb_struct = embed_structured_document(job_structured)

    scores_structured = compute_score(cv_emb_struct, job_emb_struct)

    if DEBUG:
        print("\n[DEBUG] Structured scores:", scores_structured)

    # 4️⃣ Embeddings FULL TEXT
    cv_full = {"full_text": cv_text}
    job_full = {"full_text": job_text}

    cv_emb_full = embed_structured_document(cv_full)
    job_emb_full = embed_structured_document(job_full)

    scores_full = compute_score(cv_emb_full, job_emb_full)

    if DEBUG:
        print("\n[DEBUG] Full-text scores:", scores_full)

    # 5️⃣ Fusion
    fused_scores = fuse_scores(
        scores_rules=scores_structured,
        scores_llm=scores_full,
        alpha=0.4  # poids du structuré
    )

    if DEBUG:
        print("\n[DEBUG] Fused scores:", fused_scores)

    return fused_scores, cv_structured, job_structured


# -------------------------------------------------
# RUN MATCHING (STABLE)
# -------------------------------------------------
def run_matching(cv_path, job_path, n_runs=5):
    all_scores = []
    last_cv_structured = None
    last_job_structured = None

    for i in range(n_runs):
        if DEBUG:
            print(f"\n{'#'*20} RUN {i+1}/{n_runs} {'#'*20}")

        scores, cv_structured, job_structured = single_run(cv_path, job_path)
        all_scores.append(scores)
        last_cv_structured = cv_structured
        last_job_structured = job_structured

    aggregated = {}
    stability = {}

    keys = set().union(*[s.keys() for s in all_scores])

    for k in keys:
        values = [s[k] for s in all_scores if k in s]
        aggregated[k] = mean(values)
        stability[k] = stdev(values) if len(values) > 1 else 0.0

    explanation = explain_match(
        aggregated,
        last_cv_structured,
        last_job_structured
    )

    return {
        "scores_mean": aggregated,
        "scores_std": stability,
        "explanation": explanation,
        "n_runs": n_runs
    }


# -------------------------------------------------
# CLI
# -------------------------------------------------
if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent

    result = run_matching(
        cv_path=BASE_DIR / "DATA" / "CV.pdf",
        job_path=BASE_DIR / "DATA" / "offre.txt",
        n_runs=1
    )

    print("\n==============================")
    print("FINAL MATCHING RESULT")
    print("==============================")

    for k, v in result["scores_mean"].items():
        std = result["scores_std"].get(k, 0.0)
        print(f"{k}: {v:.3f} ± {std:.3f}")

    print("\nAI Explanation:")
    print("------------------------------")
    print(result["explanation"])
