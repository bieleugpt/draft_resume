'''
from evaluation.ndcg import ndcg_at_k
from load_ground_truth import load_ground_truth

ndcg = ndcg_at_k(
    ranked_jobs,
    load_ground_truth(),
    cv_id="resume_001",
    k=10
)

print("NDCG@10:", ndcg)

'''

from data_loader import load_resumes, load_jobs
from structuring.structuring_pipeline import structure_document
from embedding.embedder import Embedder
from embedding.embedding_model import EmbeddingModel
from matching.multi_job_matching import match_cv_to_jobs
from evaluation.ndcg import ndcg_at_k
from load_ground_truth import load_ground_truth

# =========================
# Paramètres
# =========================
K = 10

# =========================
# Chargement des données
# =========================
resumes = load_resumes()
jobs = load_jobs()
ground_truth = load_ground_truth()

cv_id, cv_text = list(resumes.items())[0]

# =========================
# Structuration
# =========================
cv_structured = structure_document(cv_text, doc_type="cv")
jobs_structured = {
    job_id: structure_document(text, doc_type="job")
    for job_id, text in jobs.items()
}

# =========================
# Embeddings
# =========================
model = EmbeddingModel("sentence-transformers/all-MiniLM-L6-v2")
embedder = Embedder(model)

cv_embeddings = embedder.embed_document(cv_structured)
jobs_embeddings = {
    job_id: embedder.embed_document(job_struct)
    for job_id, job_struct in jobs_structured.items()
}

# =========================
# Ranking
# =========================
ranked_jobs = match_cv_to_jobs(
    cv_embeddings,
    jobs_embeddings
)

# =========================
# NDCG@K
# =========================
ndcg = ndcg_at_k(
    ranked_jobs=ranked_jobs,
    ground_truth=ground_truth,
    cv_id=cv_id,
    k=K
)

print(f"📊 NDCG@{K}: {ndcg:.3f}")
