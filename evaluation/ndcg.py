import math

def dcg_at_k(ranked_jobs, ground_truth, cv_id, k=10):
    dcg = 0.0

    for i, item in enumerate(ranked_jobs[:k]):
        job_id = item["job_id"]
        relevance = ground_truth.get((cv_id, job_id), 0)

        if relevance > 0:
            dcg += (2 ** relevance - 1) / math.log2(i + 2)

    return dcg


def ndcg_at_k(ranked_jobs, ground_truth, cv_id, k=10):
    actual_dcg = dcg_at_k(ranked_jobs, ground_truth, cv_id, k)

    # DCG idéal (tous les bons matchs en haut)
    relevant_jobs = [
        job_id
        for (cv, job_id), label in ground_truth.items()
        if cv == cv_id and label == 1
    ]

    if not relevant_jobs:
        return 0.0

    ideal_ranked = [{"job_id": job_id} for job_id in relevant_jobs]
    ideal_dcg = dcg_at_k(ideal_ranked, ground_truth, cv_id, k)

    return actual_dcg / ideal_dcg if ideal_dcg > 0 else 0.0
