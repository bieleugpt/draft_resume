from matching.scorer import compute_score


def match_documents(cv_embeddings, job_embeddings):
    return compute_score(cv_embeddings, job_embeddings)
