
'''
#run_ranking.py
from load_ground_truth import load_ground_truth
from matching.multi_job_matching import match_cv_to_jobs

# À ADAPTER À TON PIPELINE EXISTANT
cv_id = "resume_001"
cv_embeddings = ...              # embeddings du CV
jobs_embeddings = ...            # embeddings de TOUS les jobs
WEIGHTS = {
    "hard_skills": 0.35,
    "experience": 0.25,
    "education": 0.15,
    "tools_technologies": 0.15,
    "soft_skills": 0.10
}

ranked_jobs = match_cv_to_jobs(
    cv_embeddings,
    jobs_embeddings
)

print(ranked_jobs[:5])



'''



from embedding.embedder import Embedder
from embedding.embedding_model import EmbeddingModel
from matching.multi_job_matching import match_cv_to_jobs
from data_loader import load_resumes, load_jobs
from structuring.structuring_pipeline import structure_document

# =========================
# 1. Charger les documents
# =========================
resumes = load_resumes()
jobs = load_jobs()

# ⚠️ on prend UN CV pour le ranking
cv_id, cv_doc = list(resumes.items())[0]

# =========================
# 2. Structuration
# =========================
cv_structured = structure_document(cv_doc, doc_type="cv")
jobs_structured = {
    job_id: structure_document(text, doc_type="job")
    for job_id, text in jobs.items()
}

# =========================
# 3. Embeddings
# =========================
embedding_model = EmbeddingModel("sentence-transformers/all-MiniLM-L6-v2")
embedder = Embedder(embedding_model)

cv_embeddings = embedder.embed_document(cv_structured)
jobs_embeddings = {
    job_id: embedder.embed_document(job_struct)
    for job_id, job_struct in jobs_structured.items()
}

# =========================
# 4. Ranking
# =========================
ranked_jobs = match_cv_to_jobs(
    cv_embeddings,
    jobs_embeddings
)

# =========================
# 5. Résultat
# =========================
print("\n🏆 TOP 5 JOBS:")
for r in ranked_jobs[:5]:
    print(f"{r['job_id']} -> score = {round(r['score'], 4)}")

