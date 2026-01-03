from structuring import structure_document
from embedding import embed_structured_document
from matching.scorer import compute_score

EXPECTED_KEYS = [
    "hard_skills",
    "soft_skills",
    "tools_technologies",
    "domain_knowledge",
    "experience",
    "education"
]


def run_structured_pipeline(text: str, doc_type: str):
    structured = structure_document(text, doc_type)

    for k in EXPECTED_KEYS:
        structured.setdefault(k, "")

    embeddings = embed_structured_document(structured)
    return structured, embeddings


def score_structured(cv_text, job_text):
    cv_struct, cv_emb = run_structured_pipeline(cv_text, "cv")
    job_struct, job_emb = run_structured_pipeline(job_text, "job")

    scores = compute_score(cv_emb, job_emb)
    return scores, cv_struct, job_struct
