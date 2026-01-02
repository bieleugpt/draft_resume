from pathlib import Path

from ingestion import ingest_file
from structuring import structure_document
from embedding import embed_structured_document
from matching.scorer import compute_score   # ✅ BON IMPORT


def print_structured(title, structured):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)
    for k, v in structured.items():
        if k not in ["raw_text", "full_text"]:
            print(f"- {k}:")
            print(v if v else "[EMPTY]")


def print_embeddings(title, embeddings):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)
    for k, v in embeddings.items():
        print(f"- {k}: {'OK' if v is not None else 'NONE'}")


if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent

    cv_path = BASE_DIR / "DATA" / "CV.pdf"
    job_path = BASE_DIR / "DATA" / "offre.txt"

    # 1️⃣ Ingestion
    cv_text = ingest_file(cv_path)
    job_text = ingest_file(job_path)

    # 2️⃣ Structuration
    cv_structured = structure_document(cv_text, doc_type="cv")
    job_structured = structure_document(job_text, doc_type="job")

    print_structured("STRUCTURED CV", cv_structured)
    print_structured("STRUCTURED JOB", job_structured)

    # 3️⃣ Embeddings
    cv_embeddings = embed_structured_document(cv_structured)
    job_embeddings = embed_structured_document(job_structured)

    print_embeddings("EMBEDDINGS CV", cv_embeddings)
    print_embeddings("EMBEDDINGS JOB", job_embeddings)

    # 4️⃣ Matching (Option A active)
    scores = compute_score(cv_embeddings, job_embeddings)

    print("\n" + "=" * 50)
    print("MATCHING SCORES")
    print("=" * 50)

    for k, v in scores.items():
        print(f"{k}: {v:.3f}")
