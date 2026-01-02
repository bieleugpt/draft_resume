from embedding.embedding_model import EmbeddingModel
from evaluation.recall import recall_at_k
from matching.multi_job_matching import match_cv_to_jobs
from load_ground_truth import load_ground_truth
import time

MODELS = {
    "MiniLM": "all-MiniLM-L6-v2",
    "MPNet": "all-mpnet-base-v2"
}

def benchmark(models, dataset, weights):
    results = []

    ground_truth = load_ground_truth()

    for name, model_name in models.items():
        embedder = EmbeddingModel(model_name)
        recalls = []
        start = time.time()

        for cv_id, cv_data in dataset["cvs"].items():
            cv_embeddings = {
                sec: embedder.encode(text)
                for sec, text in cv_data.items()
            }

            jobs_embeddings = {}
            for job_id, job_data in dataset["jobs"].items():
                jobs_embeddings[job_id] = {
                    sec: embedder.encode(text)
                    for sec, text in job_data.items()
                }

            ranked_jobs = match_cv_to_jobs(
                cv_embeddings,
                jobs_embeddings,
                weights
            )

            recalls.append(
                recall_at_k(ranked_jobs, ground_truth, cv_id, k=5)
            )

        duration = time.time() - start

        results.append({
            "model": name,
            "avg_recall@5": sum(recalls) / len(recalls),
            "latency_sec": duration
        })

    return results
