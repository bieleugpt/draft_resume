
import time
from collections import defaultdict

from load_ground_truth import load_ground_truth
from LOADERS.pdf_loader import load_pdf

from embedding.embedding_model import EmbeddingModel
from matching.multi_job_matching import match_cv_to_jobs
from evaluation.recall import recall_at_k
from evaluation.ndcg import ndcg_at_k
from visualization.ranking_table import ranking_to_dataframe
from visualization.ranking_bar_chart import plot_ranking_bar_chart


# ---------------- CONFIG ----------------

CV_DIR = "DATA/resumes"
JOB_DIR = "DATA/jobs"

WEIGHTS = {
    "hard_skills": 0.35,
    "experience": 0.25,
    "education": 0.15,
    "tools_technologies": 0.15,
    "soft_skills": 0.10
}

MODELS = {
    "MiniLM": "all-MiniLM-L6-v2",
    "MPNet": "all-mpnet-base-v2"
}

# ----------------------------------------


def build_embeddings(text, embedder):
    return {
        "full_text": embedder.encode(text)
    }


def main():
    ground_truth = load_ground_truth()

    cvs = list({cv for (cv, _), label in ground_truth.items() if label == 1})
    jobs = list({job for (_, job), label in ground_truth.items()})

    print(f"Evaluating {len(cvs)} CV(s) against {len(jobs)} jobs")

    for model_name, model_id in MODELS.items():
        print("\n==============================")
        print(f"MODEL: {model_name}")
        print("==============================")

        embedder = EmbeddingModel(model_id)

        recalls = []
        ndcgs = []

        start_time = time.time()

        for cv_id in cvs:
            cv_text = load_pdf(f"{CV_DIR}/{cv_id}")
            cv_emb = build_embeddings(cv_text, embedder)

            jobs_embeddings = {}
            for job_id in jobs:
                job_text = load_pdf(f"{JOB_DIR}/{job_id}")
                jobs_embeddings[job_id] = build_embeddings(job_text, embedder)

            '''
            ranked_jobs = match_cv_to_jobs(
                cv_embeddings=cv_emb,
                jobs_embeddings=jobs_embeddings,
                weights={"full_text": 1.0}
            )
            '''
            ranked_jobs = match_cv_to_jobs(
            cv_embeddings=cv_emb,
            jobs_embeddings=jobs_embeddings
            )


            r5 = recall_at_k(ranked_jobs, ground_truth, cv_id, k=5)
            n10 = ndcg_at_k(ranked_jobs, ground_truth, cv_id, k=10)

            recalls.append(r5)
            ndcgs.append(n10)

            print(f"\nCV: {cv_id}")
            print(f"Recall@5 = {r5:.3f}")
            print(f"NDCG@10 = {n10:.3f}")

            df = ranking_to_dataframe(ranked_jobs, top_k=10)
            print(df)

            plot_ranking_bar_chart(ranked_jobs, top_k=10)

        elapsed = time.time() - start_time

        print("\n----- SUMMARY -----")
        print(f"Avg Recall@5: {sum(recalls)/len(recalls):.3f}")
        print(f"Avg NDCG@10: {sum(ndcgs)/len(ndcgs):.3f}")
        print(f"Latency: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
