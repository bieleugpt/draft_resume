
'''
#multi_job_matching.py
from matching.similarity import cosine_similarity
from matching.scorer import compute_weighted_score

def match_cv_to_jobs(
    cv_embeddings: dict,
    jobs_embeddings: dict,
    weights: dict
):
    """
    cv_embeddings: dict[str, np.array]
    jobs_embeddings: dict[job_id -> dict[str, np.array]]
    weights: dict[str, float]
    """

    rankings = []

    for job_id, job_sections in jobs_embeddings.items():
        section_scores = {}

        for section, cv_vec in cv_embeddings.items():
            job_vec = job_sections.get(section)

            if cv_vec is None or job_vec is None:
                continue

            section_scores[section] = cosine_similarity(cv_vec, job_vec)

        total_score = compute_weighted_score(section_scores, weights)

        rankings.append({
            "job_id": job_id,
            "score": total_score,
            "section_scores": section_scores
        })

    rankings.sort(key=lambda x: x["score"], reverse=True)
    return rankings

    '''















'''
from matching.scorer import compute_score

def match_cv_to_jobs(cv_embeddings, jobs_embeddings):
    """
    cv_embeddings: dict[str -> np.array]
    jobs_embeddings: dict[job_id -> dict[str -> np.array]]
    """

    rankings = []

    for job_id, job_emb in jobs_embeddings.items():
        scores = compute_score(cv_embeddings, job_emb)

        rankings.append({
            "job_id": job_id,
            "score": scores["total"],
            "section_scores": scores
        })

    rankings.sort(key=lambda x: x["score"], reverse=True)
    return rankings

    '''



# multi_job_matching.py

from matching.scorer import compute_score

def match_cv_to_jobs(cv_embeddings, jobs_embeddings):
    rankings = []

    for job_id, job_emb in jobs_embeddings.items():
        scores = compute_score(cv_embeddings, job_emb)

        rankings.append({
            "job_id": job_id,
            "score": scores["total"],
            "details": scores
        })

    rankings.sort(key=lambda x: x["score"], reverse=True)
    return rankings




