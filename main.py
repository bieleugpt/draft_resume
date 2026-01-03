DEBUG = True

# =========================
# DEBUG HELPERS
# =========================

def debug_title(title: str):
    if not DEBUG:
        return
    print("\n" + "=" * 70)
    print(f"[DEBUG] {title}")
    print("=" * 70)


def debug_kv(key: str, value):
    if not DEBUG:
        return
    print(f"- {key}: {value}")


def debug_dict(title: str, d: dict):
    if not DEBUG:
        return
    debug_title(title)
    for k, v in d.items():
        print(f"{k}:")
        print(v if v else "[EMPTY]")


# =========================
# PIPELINE IMPORTS
# =========================

from ingestion import ingest_file
from statistics import mean, stdev

from pipelines.structured_pipeline import score_structured
from pipelines.fulltext_pipeline import score_fulltext
from pipelines.fusion import fuse_scores
from explanation import explain_match


# =========================
# CORE PIPELINE
# =========================

def run_matching(cv_path, job_path, n_runs=5):
    all_scores = []

    last_cv_struct = None
    last_job_struct = None
    last_cv_full = ""
    last_job_full = ""

    for i in range(n_runs):
        debug_title(f"RUN {i+1}/{n_runs}")

        cv_text = ingest_file(cv_path)
        job_text = ingest_file(job_path)

        debug_kv("CV text length", len(cv_text))
        debug_kv("Job text length", len(job_text))

        scores_struct, cv_struct, job_struct = score_structured(cv_text, job_text)
        scores_full, cv_full, job_full = score_fulltext(cv_text, job_text)

        debug_dict("STRUCTURED CV", cv_struct)
        debug_dict("STRUCTURED JOB", job_struct)

        debug_kv("FULL TEXT CV (preview)", cv_full[:200] + "...")
        debug_kv("FULL TEXT JOB (preview)", job_full[:200] + "...")

        debug_dict("STRUCTURED SCORES", scores_struct)
        debug_dict("FULL-TEXT SCORES", scores_full)

        fused = fuse_scores(scores_struct, scores_full, alpha=0.4)
        debug_dict("FUSED SCORES", fused)

        all_scores.append(fused)

        last_cv_struct = cv_struct
        last_job_struct = job_struct
        last_cv_full = cv_full
        last_job_full = job_full

    # =========================
    # AGGREGATION
    # =========================

    aggregated = {}
    stability = {}

    keys = set().union(*all_scores)

    debug_title("AGGREGATED RESULTS (MEAN ± STD)")

    for k in keys:
        values = [s[k] for s in all_scores if k in s]
        aggregated[k] = mean(values)
        stability[k] = stdev(values) if len(values) > 1 else 0.0
        print(f"{k:20s}: {aggregated[k]:.3f} ± {stability[k]:.3f}")

    explanation = explain_match(
        aggregated,
        last_cv_struct,
        last_job_struct
    )

    return {
        "scores_mean": aggregated,
        "scores_std": stability,
        "cv_structured": last_cv_struct,
        "job_structured": last_job_struct,
        "cv_full_view": last_cv_full,
        "job_full_view": last_job_full,
        "explanation": explanation
    }


# =========================
# CLI DEBUG ENTRY POINT
# =========================

if __name__ == "__main__":
    from pathlib import Path

    debug_title("MAIN DEBUG EXECUTION")

    BASE_DIR = Path(__file__).parent
    cv_path = BASE_DIR / "DATA" / "CV.pdf"
    job_path = BASE_DIR / "DATA" / "offre.txt"

    result = run_matching(
        cv_path=cv_path,
        job_path=job_path,
        n_runs=3
    )

    debug_dict("FINAL STRUCTURED CV", result["cv_structured"])
    debug_dict("FINAL STRUCTURED JOB", result["job_structured"])

    debug_kv("FINAL FULL TEXT CV", result["cv_full_view"][:300] + "...")
    debug_kv("FINAL FULL TEXT JOB", result["job_full_view"][:300] + "...")

    debug_title("AI EXPLANATION")
    print(result["explanation"])

    debug_title("END OF DEBUG RUN")
