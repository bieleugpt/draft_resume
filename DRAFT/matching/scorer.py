# matching/scorer.py

from matching.similarity import cosine_similarity

print("SCORER FILE USED:", __file__)

WEIGHTS = {
    "hard_skills": 0.35,
    "soft_skills": 0.15,
    "tools_technologies": 0.2,
    "domain_knowledge": 0.15,
    "experience": 0.1,
    "education": 0.05,
    "full_text": 0.2,
}


def compute_score(cv_embeddings, job_embeddings):
    scores = {}
    weighted_sum = 0.0
    weight_sum = 0.0

    for key, weight in WEIGHTS.items():
        cv_emb = cv_embeddings.get(key)
        job_emb = job_embeddings.get(key)

        if cv_emb is None or job_emb is None:
            continue

        try:
            sim = float(cosine_similarity(cv_emb, job_emb))
            scores[key] = sim
            weighted_sum += weight * sim
            weight_sum += weight
        except Exception:
            continue

    scores["total"] = weighted_sum / weight_sum if weight_sum > 0 else 0.0

    # DEBUG TRACE
    print("[DEBUG] CV embeddings:", {k: v is not None for k, v in cv_embeddings.items()})
    print("[DEBUG] JOB embeddings:", {k: v is not None for k, v in job_embeddings.items()})

    return scores
