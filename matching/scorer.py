'''

from typing import Dict
from matching.similarity import cosine_similarity


DEFAULT_WEIGHTS = {
    "skills": 0.4,
    "experience": 0.4,
    "education": 0.2
}


def compute_score(cv_embeddings, job_embeddings, weights=DEFAULT_WEIGHTS):
    scores = {}
    total_score = 0.0

    for section, weight in weights.items():
        sim = cosine_similarity(
            cv_embeddings.get(section),
            job_embeddings.get(section)
        )

        # bonus faible pour education si non nulle
        if section == "education" and sim < 0.1:
            sim = 0.1

        scores[section] = sim
        total_score += weight * sim

    scores["total"] = total_score
    return scores
'''



#scorer.py
from matching.similarity import cosine_similarity


WEIGHTS = {
    "hard_skills": 0.4,
    "tools_technologies": 0.2,
    "domain_knowledge": 0.2,
    "soft_skills": 0.2,
    "experience": 0.3,
    "education": 0.1,
}


def compute_score(cv_embeddings, job_embeddings):
    scores = {}
    total = 0.0
    weight_sum = 0.0
    WEIGHTS = {
    "full_text": 1.0
    }


    for key, weight in WEIGHTS.items():
        if cv_embeddings.get(key) is not None and job_embeddings.get(key) is not None:
            sim = cosine_similarity(
                cv_embeddings[key],
                job_embeddings[key]
            )
            scores[key] = sim
            total += weight * sim
            weight_sum += weight

    scores["total"] = total / weight_sum if weight_sum > 0 else 0.0
    print({k: (v is not None) for k, v in cv_embeddings.items()})
    print({k: (v is not None) for k, v in job_embeddings.items()})

    return scores


