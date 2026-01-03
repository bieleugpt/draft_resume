
#scorer.py
from matching.similarity import cosine_similarity
import numpy as np

MATCH_KEYS = [
    "hard_skills",
    "soft_skills",
    "tools_technologies",
    "domain_knowledge",
    "experience",
    "education",
    "full_text"
]

WEIGHTS = {
    "hard_skills": 0.25,
    "soft_skills": 0.15,
    "tools_technologies": 0.15,
    "domain_knowledge": 0.15,
    "experience": 0.15,
    "education": 0.05,
    "full_text": 0.10
}


def compute_score(cv_embeddings, job_embeddings):
    scores = {}
    weighted_scores = []
    weights_used = []

    for key in MATCH_KEYS:
        cv_emb = cv_embeddings.get(key)
        job_emb = job_embeddings.get(key)
        weight = WEIGHTS.get(key, 0)

        if cv_emb is None or job_emb is None:
            continue

        sim = float(cosine_similarity(cv_emb, job_emb))
        scores[key] = sim
        weighted_scores.append(sim * weight)
        weights_used.append(weight)

    scores["total"] = (
        sum(weighted_scores) / sum(weights_used)
        if weights_used else 0.0
    )

    return scores
