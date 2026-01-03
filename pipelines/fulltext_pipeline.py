from embedding import embed_structured_document
from matching.scorer import compute_score


def extract_fulltext_view(text: str, max_len: int = 600):
    return text[:max_len]


def score_fulltext(cv_text, job_text):
    cv_view = extract_fulltext_view(cv_text)
    job_view = extract_fulltext_view(job_text)

    cv_emb = embed_structured_document({"full_text": cv_text})
    job_emb = embed_structured_document({"full_text": job_text})

    scores = compute_score(cv_emb, job_emb)
    return scores, cv_view, job_view
