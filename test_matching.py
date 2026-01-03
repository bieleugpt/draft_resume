
#test_matching.py
from pathlib import Path
from ingestion import ingest_file
from structuring import structure_document
from embedding import embed_structured_document
from matching.scorer import compute_score


def print_structured(title, structured):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)
    for k, v in structured.items():
        if k not in ["raw_text", "full_text"]:
            print(f"- {k}: {v if v else '[EMPTY]'}")


if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent

    cv_text = ingest_file(BASE_DIR / "DATA" / "CV.pdf")
    job_text = ingest_file(BASE_DIR / "DATA" / "offre.txt")

    cv_structured = structure_document(cv_text, "cv")
    job_structured = structure_document(job_text, "job")

    print_structured("STRUCTURED CV", cv_structured)
    print_structured("STRUCTURED JOB", job_structured)

    cv_emb = embed_structured_document(cv_structured)
    job_emb = embed_structured_document(job_structured)

    scores = compute_score(cv_emb, job_emb)

    print("\nMATCHING SCORES")
    for k, v in scores.items():
        print(f"{k}: {v:.3f}")
