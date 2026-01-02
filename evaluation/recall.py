def recall_at_k(ranked_jobs, ground_truth, cv_id, k=5):
    """
    ranked_jobs: list of dicts (sorted)
    ground_truth: dict[(cv_id, job_id)] -> 0/1
    """

    top_k = ranked_jobs[:k]

    relevant_jobs = {
        job_id
        for (cv, job_id), label in ground_truth.items()
        if cv == cv_id and label == 1
    }

    if not relevant_jobs:
        return 0.0

    retrieved_jobs = {item["job_id"] for item in top_k}
    true_positives = relevant_jobs & retrieved_jobs

    return len(true_positives) / len(relevant_jobs)
