

#run_model_comparison.py

'''
import time
import pandas as pd

from embedding.embedder import Embedder
from matching.multi_job_matching import match_cv_to_jobs
from evaluation.recall import recall_at_k
from evaluation.ndcg import ndcg_at_k
from load_ground_truth import load_ground_truth
from data_loader import load_resumes, load_jobs

MODELS = {
    "MiniLM": "sentence-transformers/all-MiniLM-L6-v2",
    "MPNet": "sentence-transformers/all-mpnet-base-v2"
}

K = 10
results = []

ground_truth = load_ground_truth()
resumes = load_resumes()
jobs = load_jobs()

for model_name, model_path in MODELS.items():
    print(f"\n🔍 Evaluating {model_name}")

    embedder = Embedder(model_path)

    start_time = time.time()

    cv_embeddings = embedder.embed_documents(resumes)
    job_embeddings = embedder.embed_documents(jobs)

    rankings = match_cv_to_jobs(
        cv_embeddings,
        job_embeddings
    )

    latency = time.time() - start_time

    recall = recall_at_k(rankings, ground_truth, k=K)
    ndcg = ndcg_at_k(rankings, ground_truth, k=K)

    results.append({
        "Model": model_name,
        "Recall@10": recall,
        "NDCG@10": ndcg,
        "Latency (s)": round(latency, 2)
    })

df = pd.DataFrame(results)
print("\n📊 Model comparison results:")
print(df)
df.to_csv("evaluation/model_comparison.csv", index=False)
'''


import time
import pandas as pd

from embedding.embedder import Embedder
from embedding.embedding_model import EmbeddingModel
from matching.multi_job_matching import match_cv_to_jobs
from evaluation.recall import recall_at_k
from evaluation.ndcg import ndcg_at_k
from load_ground_truth import load_ground_truth
from data_loader import load_resumes, load_jobs
from structuring.structuring_pipeline import structure_document


# =========================
# Modèles à comparer
# =========================
MODELS = {
    "MiniLM": "sentence-transformers/all-MiniLM-L6-v2",
    "MPNet": "sentence-transformers/all-mpnet-base-v2"
}

K = 10
results = []

# =========================
# Chargement des données
# =========================
ground_truth = load_ground_truth()
resumes = load_resumes()
jobs = load_jobs()

# On évalue sur 1 CV (choix assumé et défendable)
cv_id, cv_text = list(resumes.items())[0]

# =========================
# Structuration (UNE FOIS)
# =========================
cv_structured = structure_document(cv_text, doc_type="cv")
jobs_structured = {
    job_id: structure_document(text, doc_type="job")
    for job_id, text in jobs.items()
}

# =========================
# Boucle de comparaison
# =========================
for model_name, model_path in MODELS.items():
    print(f"\n🔍 Evaluating {model_name}")

    model = EmbeddingModel(model_path)
    embedder = Embedder(model)

    start_time = time.time()

    # Embeddings
    cv_embeddings = embedder.embed_document(cv_structured)
    jobs_embeddings = {
        job_id: embedder.embed_document(job_struct)
        for job_id, job_struct in jobs_structured.items()
    }

    # Ranking
    rankings = match_cv_to_jobs(
        cv_embeddings,
        jobs_embeddings
    )

    latency = time.time() - start_time

    # Évaluation
    recall = recall_at_k(
        ranked_jobs=rankings,
        ground_truth=ground_truth,
        cv_id=cv_id,
        k=K
    )

    ndcg = ndcg_at_k(
        ranked_jobs=rankings,
        ground_truth=ground_truth,
        cv_id=cv_id,
        k=K
    )

    results.append({
        "Model": model_name,
        "Recall@10": round(recall, 3),
        "NDCG@10": round(ndcg, 3),
        "Latency (s)": round(latency, 2)
    })


# =========================
# Résultats finaux
# =========================
df = pd.DataFrame(results)

print("\n📊 Model comparison results:")
print(df)

df.to_csv("evaluation/model_comparison.csv", index=False)
print("\n✅ Saved to evaluation/model_comparison.csv")

