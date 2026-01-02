# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\app.py

import csv
from pathlib import Path
from LOADERS.pdf_loader import load_pdf

RESUMES_DIR = Path("DATA/resumes")
JOBS_DIR = Path("DATA/jobs")
GT_FILE = Path("DATA/ground_truth.csv")


def save(rows):
    with GT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cv_id", "job_id", "match"])
        writer.writeheader()
        writer.writerows(rows)


def main():
    with GT_FILE.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for i, row in enumerate(rows):
        if row["match"] != "-1":
            continue

        cv_path = RESUMES_DIR / row["cv_id"]
        job_path = JOBS_DIR / row["job_id"]

        cv_text = load_pdf(str(cv_path))
        job_text = load_pdf(str(job_path))

        print("\n" + "=" * 100)
        print(f"[{i+1}/{len(rows)}]")
        print("CV:", row["cv_id"])
        print(cv_text[:1000])

        print("\nJOB:", row["job_id"])
        print(job_text[:1000])
        print("=" * 100)

        label = input("Match? (1 = yes, 0 = no): ").strip()
        while label not in {"0", "1"}:
            label = input("Please enter 1 or 0: ").strip()

        row["match"] = label
        save(rows)  # 🔥 SAUVEGARDE IMMÉDIATE

        print("✔ Saved")

    print("✅ Annotation finished")


if __name__ == "__main__":
    main()





# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\app.py

import streamlit as st
from pathlib import Path
import tempfile

from main import run_matching

# -------------------------
# Config page
# -------------------------
st.set_page_config(
    page_title="Smart Resume & Job Matcher",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Smart Resume & Job Matcher")
st.write("Matching intelligent entre un CV et une offre d’emploi")

st.divider()

# -------------------------
# Upload fichiers
# -------------------------
st.subheader("1️⃣ Charger les fichiers")

cv_file = st.file_uploader(
    "Uploader le CV (PDF)",
    type=["pdf"]
)

job_file = st.file_uploader(
    "Uploader l'offre d'emploi (TXT ou PDF)",
    type=["txt", "pdf"]
)

st.divider()

# -------------------------
# Bouton lancement
# -------------------------
st.subheader("2️⃣ Lancer le matching")

run_button = st.button("🚀 Lancer l’analyse")

# -------------------------
# Traitement
# -------------------------
if run_button:
    if cv_file is None or job_file is None:
        st.error("⚠️ Veuillez uploader le CV et l'offre d'emploi.")
    else:
        with st.spinner("Analyse en cours..."):
            # Sauvegarde temporaire des fichiers
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_dir = Path(tmp_dir)

                cv_path = tmp_dir / cv_file.name
                job_path = tmp_dir / job_file.name

                cv_path.write_bytes(cv_file.getbuffer())
                job_path.write_bytes(job_file.getbuffer())

                # Appel du pipeline IA
                result = run_matching(
                    cv_path=str(cv_path),
                    job_path=str(job_path)
                )

        st.success("✅ Analyse terminée")

        # -------------------------
        # Résultats
        # -------------------------
        st.divider()
        st.subheader("📊 Résultats du matching")

        scores_mean = result["scores_mean"]
        scores_std = result["scores_std"]
        n_runs = result["n_runs"]

        col1, col2, col3 = st.columns(3)

        total_mean = float(scores_mean.get("total", 0))
        total_std = float(scores_std.get("total", 0))

        percentage = round(total_mean * 100, 1)
        percentage_std = round(total_std * 100, 1)


        col1.metric(
            "Matching global",
            f"{percentage} %",
            f"± {percentage_std} %"
        )

        col2.metric(
            "Hard skills",
            round(scores_mean.get("hard_skills", 0), 3)
        )

        col3.metric(
            "Soft skills",
            round(scores_mean.get("soft_skills", 0), 3)
        )


        st.progress(total_mean)

        # -------------------------
        # Explication IA
        # -------------------------
        st.info(
            f"Score estimé à partir de {n_runs} exécutions indépendantes. "
            "De légères variations sont normales."
        )

        st.divider()
        st.subheader("🧠 Explication IA")

        st.write(result["explanation"])

import streamlit as st
from visualization.ranking_table import ranking_to_dataframe
from visualization.ranking_bar_chart import plot_ranking_bar_chart

st.subheader("Top Job Matches")

df = ranking_to_dataframe(ranked_jobs, top_k=10)
st.dataframe(df)

st.subheader("Ranking Visualization")
st.pyplot(plot_ranking_bar_chart(ranked_jobs, top_k=10))






# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\check_ground_truth.py

import csv
from collections import defaultdict

GT_FILE = "DATA/ground_truth.csv"

def main():
    cv_counts = defaultdict(int)
    job_counts = defaultdict(int)
    total = 0
    positives = 0

    with open(GT_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            if row["match"] == "1":
                positives += 1
                cv_counts[row["cv_id"]] += 1
                job_counts[row["job_id"]] += 1

    print("Total pairs:", total)
    print("Positive matches:", positives)
    print("Positive ratio:", positives / total if total else 0)

    print("\nMatches per CV:")
    for cv, count in cv_counts.items():
        print(f"{cv}: {count}")

    print("\nMatches per Job:")
    for job, count in job_counts.items():
        print(f"{job}: {count}")

if __name__ == "__main__":
    main()






# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\data_loader.py

from pathlib import Path
from LOADERS.pdf_loader import load_pdf

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "DATA"
RESUMES_DIR = DATA_DIR / "resumes"
JOBS_DIR = DATA_DIR / "jobs"


def load_resumes():
    resumes = {}
    for pdf in RESUMES_DIR.glob("*.pdf"):
        resumes[pdf.name] = load_pdf(pdf)
    return resumes


def load_jobs():
    jobs = {}
    for pdf in JOBS_DIR.glob("*.pdf"):
        jobs[pdf.name] = load_pdf(pdf)
    return jobs




# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\dataset_utils.py

from pathlib import Path

def list_pdfs(directory: str):
    return sorted([
        p for p in Path(directory).iterdir()
        if p.suffix.lower() == ".pdf"
    ])





# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\generate_ground_truth_template.py

import csv
from dataset_utils import list_pdfs

RESUMES_DIR = "DATA/resumes"
JOBS_DIR = "DATA/jobs"
OUTPUT_FILE = "DATA/ground_truth.csv"

def main():
    resumes = list_pdfs(RESUMES_DIR)
    jobs = list_pdfs(JOBS_DIR)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["cv_id", "job_id", "match"])

        for cv in resumes:
            for job in jobs:
                writer.writerow([cv.name, job.name, -1])

    print(f"Ground truth created with {len(resumes)} CVs × {len(jobs)} jobs")

if __name__ == "__main__":
    main()





# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\load_ground_truth.py

import csv

def load_ground_truth(path="DATA/ground_truth.csv"):
    gt = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["cv_id"], row["job_id"])
            gt[key] = int(row["match"])

    return gt

if __name__ == "__main__":
    gt = load_ground_truth()
    print("Loaded ground truth pairs:", len(gt))





# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\main.py

from ingestion import ingest_file
from structuring import structure_document
from embedding import embed_structured_document
from matching import match_documents
from explanation import explain_match

from pathlib import Path
import random
import numpy as np
import torch
from statistics import mean, stdev

# -----------------------------
# Reproductibilité contrôlée
# -----------------------------
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

EXPECTED_KEYS = [
    "hard_skills",
    "soft_skills",
    "tools_technologies",
    "domain_knowledge",
    "experience",
    "education"
]

# -----------------------------
# Pipeline unitaire
# -----------------------------
def single_run(cv_path, job_path):
    # Ingestion
    cv_text = ingest_file(cv_path)
    job_text = ingest_file(job_path)

    # Structuration
    cv_structured = structure_document(cv_text, doc_type="cv")
    job_structured = structure_document(job_text, doc_type="job")

    # 🔒 Figer la structure textuelle
    for key in EXPECTED_KEYS:
        cv_structured.setdefault(key, "")
        job_structured.setdefault(key, "")

    # Embeddings
    cv_embeddings = embed_structured_document(cv_structured)
    job_embeddings = embed_structured_document(job_structured)

    # 🔒 Figer les clés embeddings
    for key in EXPECTED_KEYS:
        cv_embeddings.setdefault(key, None)
        job_embeddings.setdefault(key, None)

    # Matching
    scores = match_documents(job_embeddings, cv_embeddings)

    return scores, cv_structured, job_structured


# -----------------------------
# Matching avec stabilité
# -----------------------------
def run_matching(cv_path, job_path, n_runs=5):
    """
    Lance plusieurs matching successifs pour estimer :
    - score moyen
    - variabilité (incertitude)
    """

    all_scores = []
    last_cv_structured = None
    last_job_structured = None

    for _ in range(n_runs):
        scores, cv_structured, job_structured = single_run(cv_path, job_path)
        all_scores.append(scores)
        last_cv_structured = cv_structured
        last_job_structured = job_structured

    # Agrégation
    aggregated_scores = {}
    stability = {}

    # 🔒 Union de toutes les clés rencontrées
    all_keys = set()
    for s in all_scores:
        all_keys.update(s.keys())

    aggregated_scores = {}
    stability = {}

    for key in all_keys:
        values = [s.get(key, 0.0) for s in all_scores]

        aggregated_scores[key] = mean(values)
        stability[key] = stdev(values) if len(values) > 1 else 0.0

    # Explication basée sur le score moyen
    explanation = explain_match(
        aggregated_scores,
        last_cv_structured,
        last_job_structured
    )

    return {
        "scores_mean": aggregated_scores,
        "scores_std": stability,
        "explanation": explanation,
        "n_runs": n_runs
    }

# -----------------------------
# Mode CLI (test local)
# -----------------------------
if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent

    cv_path = BASE_DIR / "DATA" / "CV.pdf"
    job_path = BASE_DIR / "DATA" / "offre.txt"

    result = run_matching(cv_path, job_path, n_runs=5)

    print("\n==============================")
    print("MATCHING RESULT (ESTIMATION)")
    print("==============================")

    for k, v in result["scores_mean"].items():
        std = result["scores_std"][k]
        print(f"{k}: {v:.3f} ± {std:.3f}")

    print("\nAI Explanation:")
    print("------------------------------")
    print(result["explanation"])





# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\run_evaluation.py

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






# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\run_model_comparison.py

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







# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\run_ndcg.py

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






#C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\run_ranking.py

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





# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\run_recall.py

from data_loader import load_resumes, load_jobs
from structuring.structuring_pipeline import structure_document
from embedding.embedder import Embedder
from embedding.embedding_model import EmbeddingModel
from matching.multi_job_matching import match_cv_to_jobs
from evaluation.recall import recall_at_k
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

# 1 CV pour l'évaluation
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
# Recall@K
# =========================
recall = recall_at_k(
    ranked_jobs=ranked_jobs,
    ground_truth=ground_truth,
    cv_id=cv_id,
    k=K
)

print(f"📊 Recall@{K}: {recall:.3f}")





# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\visualization\ranking_table.py
import pandas as pd

def ranking_to_dataframe(ranked_jobs, top_k=10):
    data = []

    for item in ranked_jobs[:top_k]:
        data.append({
            "Job ID": item["job_id"],
            "Score": round(item["score"], 3)
        })

    return pd.DataFrame(data)






# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\visualization\ranking_bar_chart.py
import matplotlib.pyplot as plt

def plot_ranking_bar_chart(ranked_jobs, top_k=10):
    jobs = [item["job_id"] for item in ranked_jobs[:top_k]]
    scores = [item["score"] for item in ranked_jobs[:top_k]]

    #plt.figure(figsize=(10, 6))

    plt.figure()
    plt.barh(jobs, scores)
    plt.xlabel("Matching Score")
    plt.ylabel("Job ID")
    plt.title("Top Job Matches")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()






C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\structuring\structuring_pipeline.py

# structuring_pipeline.py

from typing import Dict
import re

from structuring.section_extractor import extract_sections
from structuring.skill_extractor_2 import SkillExtractor
from llm.ollama_client import OllamaClient
from sentence_transformers import SentenceTransformer
from matching.similarity import cosine_similarity


# =========================
# LLM (skills extraction)
# =========================
llm = OllamaClient(model="mistral:7b")


# =========================
# Semantic model (tools)
# =========================
_semantic_model = SentenceTransformer("all-mpnet-base-v2")
_TECH_CONCEPT = _semantic_model.encode(
    "software tools and technologies used in data analysis and business intelligence"
)


# =====================================================
# JOB EXPERIENCE EXTRACTION (rules, dynamic)
# =====================================================
def extract_job_experience(text: str):
    patterns = [
        r"(\d+\s*(?:à|-)\s*\d+\s*ans?)",
        r"(\d+\+?\s*ans?)",
        r"(poste\s+équivalent)",
        r"(expérience\s+significative)",
        r"(junior|confirmé|senior)",
    ]

    matches = []
    for p in patterns:
        matches.extend(re.findall(p, text, flags=re.IGNORECASE))

    return " ".join(set(matches)) if matches else None


# =====================================================
# JOB EDUCATION EXTRACTION (rules, dynamic)
# =====================================================
def extract_job_education(text: str):
    patterns = [
        r"(bac\s*\+\s*\d)",
        r"(bac\s*\+\s*\d\s*(?:à|-)\s*bac\s*\+\s*\d)",
        r"(niveau\s+bac\s*\+\s*\d)",
        r"(dipl[oô]me\s+requis)",
        r"(formation\s+(?:informatique|scientifique|data))",
    ]

    matches = []
    for p in patterns:
        matches.extend(re.findall(p, text, flags=re.IGNORECASE))

    return " ".join(set(matches)) if matches else None


# =====================================================
# TOOLS & TECHNOLOGIES EXTRACTION (dynamic + semantic)
# =====================================================
def extract_candidate_tools(text: str):
    patterns = [
        r"(?:tools?|technologies?|logiciels?|frameworks?)\s+(?:tels que|comme|including)?\s*([A-Za-z0-9+.,\-\s/]+)",
        r"(?:ma[iî]trise|exp[eé]rience)\s+(?:de|avec|en)\s+([A-Za-z0-9+.,\-\s/]+)",
    ]

    candidates = []
    for p in patterns:
        matches = re.findall(p, text, flags=re.IGNORECASE)
        for m in matches:
            parts = re.split(r",|et|and|/|\|", m)
            candidates.extend([p.strip() for p in parts if len(p.strip()) > 2])

    return list(set(candidates))


def filter_tools_semantically(candidates, threshold=0.35):
    tools = []
    for c in candidates:
        emb = _semantic_model.encode(c)
        if cosine_similarity(emb, _TECH_CONCEPT) >= threshold:
            tools.append(c)
    return tools


def extract_tools_technologies(text: str):
    candidates = extract_candidate_tools(text)
    tools = filter_tools_semantically(candidates)
    return tools if tools else []


# =====================================================
# MAIN STRUCTURING FUNCTION
# =====================================================
def structure_document(text: str, doc_type: str) -> Dict:
    """
    doc_type: "cv" or "job"
    """
    sections = extract_sections(text)
    '''skill_extractor = SkillExtractor(llm)'''

    skills_text = sections.get("skills", "").strip()
    experience_text = sections.get("experience", "").strip()

    extraction_source = skills_text if skills_text else experience_text
    '''skills = skill_extractor.extract(extraction_source)'''



    skills = {
    "hard_skills": [],
    "soft_skills": [],
    "domain_knowledge": []
    }

    # Normalize skills
    hard_skills = skills.get("hard_skills", [])
    soft_skills = skills.get("soft_skills", [])
    domain_knowledge = skills.get("domain_knowledge", [])

    # Tools (CV + JOB, dynamic)
    tools_technologies = extract_tools_technologies(text)

    # Experience & education differ by document type
    if doc_type == "job":
        experience = extract_job_experience(text)
        education = extract_job_education(text)
    else:
        experience = experience_text
        education = sections.get("education", "").strip()

    '''
    return {
        "hard_skills": hard_skills,
        "soft_skills": soft_skills,
        "domain_knowledge": domain_knowledge,
        "tools_technologies": tools_technologies,
        "experience": experience,
        "education": education,
        "raw_text": text
    }
    '''

    '''return {
        "skills": {
            "hard_skills": hard_skills,
            "soft_skills": soft_skills,
            "domain_knowledge": domain_knowledge,
            "tools_technologies": tools_technologies,
        },
        "experience": experience,
        "education": education,
        "raw_text": text
    }'''

    return {
        "raw_text": text,
        "experience": experience,
        "education": education
    }






C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\structuring\skill_extractor_2.py

import json
import re
from typing import Dict, List

class SkillExtractor:
    def __init__(self, llm_client):
        self.llm = llm_client

    # =========================
    # Public API
    # =========================
    def extract(self, text: str) -> Dict[str, List[str]]:
        if not text.strip():
            return self._empty_skills()

        # 1️⃣ Initial extraction
        prompt = self._build_prompt(text)
        response = self.llm.generate(prompt)

        skills = self._safe_parse(response)

        # 2️⃣ Optional validation (non-blocking)
        skills = self._validate_with_llm_safe(skills)

        return self._clean_output(skills)

    # =========================
    # LLM validation (SAFE)
    # =========================
    def _validate_with_llm_safe(self, skills: Dict) -> Dict:
        prompt = f"""
You are a strict JSON validator.

You must return ONLY a valid JSON object.
No explanations. No markdown. No comments.

Schema:
{{
  "hard_skills": [string],
  "soft_skills": [string],
  "tools_technologies": [string],
  "domain_knowledge": [string]
}}

Validate and clean the following skills.
Remove irrelevant items.
Do NOT add new skills.

Input:
{json.dumps(skills)}
"""

        response = self.llm.generate(prompt)

        validated = self._safe_parse(response)

        # Fallback: if validation fails, keep original
        return validated if validated else skills

    # =========================
    # Robust JSON parsing
    # =========================
    def _safe_parse(self, text: str) -> Dict:
        # 1️⃣ Try direct JSON
        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        # 2️⃣ Try to extract JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

        # 3️⃣ Ultimate fallback
        return self._empty_skills()

    # =========================
    # Prompt
    # =========================
    def _build_prompt(self, text: str) -> str:
        return f"""
You are a strict JSON generator.

Return ONLY a valid JSON object.
Do not add explanations, comments, or markdown.

Schema:
{{
  "hard_skills": [],
  "soft_skills": [],
  "tools_technologies": [],
  "domain_knowledge": []
}}

Extract real professional skills from the following document.
Do NOT invent skills.

Document:
\"\"\"
{text}
\"\"\"
"""

    # =========================
    # Utils
    # =========================
    def _empty_skills(self) -> Dict[str, List[str]]:
        return {
            "hard_skills": [],
            "soft_skills": [],
            "tools_technologies": [],
            "domain_knowledge": []
        }

    def _clean_output(self, skills: Dict) -> Dict[str, List[str]]:
        cleaned = {}
        for key in [
            "hard_skills",
            "soft_skills",
            "tools_technologies",
            "domain_knowledge",
        ]:
            values = skills.get(key, [])
            if isinstance(values, list):
                cleaned[key] = list(
                    set(
                        v.strip()
                        for v in values
                        if isinstance(v, str) and v.strip()
                    )
                )
            else:
                cleaned[key] = []
        return cleaned







# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\structuring\skill_extractor_2(ORIGINE).py

# skill_extractor_2.py

import json
import re
from typing import Dict, List


class SkillExtractor:
    def __init__(self, llm_client):
        self.llm = llm_client

    def extract(self, text: str) -> Dict[str, List[str]]:
        if not text.strip():
            return {
                "hard_skills": [],
                "soft_skills": [],
                "tools_technologies": [],
                "domain_knowledge": []
            }

        prompt = self._build_prompt(text)
        response = self.llm.generate(prompt)

        json_text = self._extract_json(response)

        try:
            skills = json.loads(json_text)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse JSON.\nExtracted JSON:\n{json_text}\n\nFull response:\n{response}"
            ) from e

        return self._clean_output(skills)

    def _extract_json(self, text: str) -> str:
        """
        Extract the first JSON object found in the LLM response.
        """
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError(
                f"No JSON object found in LLM response:\n{text}"
            )
        return match.group(0)

    def _build_prompt(self, text: str) -> str:
        return f"""
You are an expert HR analyst.

Your task is to extract professional skills from the following document.
The document can belong to any sector (IT, finance, marketing, healthcare, law, education, etc.).

Instructions:
- Extract only real and relevant skills explicitly or implicitly mentioned.
- Do NOT invent skills.
- Group skills into meaningful categories.
- Be concise and precise.

Return the result strictly in valid JSON with this structure:

{{
  "hard_skills": [],
  "soft_skills": [],
  "tools_technologies": [],
  "domain_knowledge": []
}}

Document:
\"\"\"
{text}
\"\"\"
"""

    def _clean_output(self, skills: Dict) -> Dict[str, List[str]]:
        cleaned = {}
        for key in [
            "hard_skills",
            "soft_skills",
            "tools_technologies",
            "domain_knowledge",
        ]:
            values = skills.get(key, [])
            if isinstance(values, list):
                cleaned[key] = list(
                    set(v.strip() for v in values if isinstance(v, str) and v.strip())
                )
            else:
                cleaned[key] = []
        return cleaned





# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\structuring\skill_extractor.py
from typing import List


KNOWN_SKILLS = [
    "python", "sql", "java", "machine learning", "deep learning",
    "data analysis", "docker", "kubernetes", "aws", "gcp", "azure"
]


def extract_skills(text: str) -> List[str]:
    """
    Extract explicit skills from text using keyword matching.

    Args:
        text (str): Input text

    Returns:
        List[str]: Detected skills
    """
    text_lower = text.lower()
    skills_found = []

    for skill in KNOWN_SKILLS:
        if skill in text_lower:
            skills_found.append(skill)

    return list(set(skills_found))

'''

file = "C:\\Users\\biele\\Desktop\\Cours\\SousWindowsRodolphe\\LLM\\PROJECT\\DRAFT\\DATA\\offre.txt"
with open(file, "r", encoding="utf-8") as f:
    text = f.read() 
skills = extract_skills(text)
for skill in skills:
    print(f"--- {skill.upper()} ---")
    print(skill[:500])  # Print first 500 characters of each skill
    print() 

'''







C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\structuring\section_extractor.py
import re
from typing import Dict



SECTION_PATTERNS = {
    "skills": r"(skills|competencies|technical skills|Vous maitrisez)",
    "experience": r"(experience|work experience|professional experience|le profil recherché|profil recherché|votre profil|Vous possédez|vous avez|une expérience)",
    "education": r"(education|academic background|studies|titulaire|diplômé de|diplômée de)",
}


def extract_sections(text: str) -> Dict[str, str]:
    """
    Extract main sections from a CV or job description.

    Args:
        text (str): Cleaned input text

    Returns:
        Dict[str, str]: Sections mapped to their content
    """
    sections = {key: "" for key in SECTION_PATTERNS}
    current_section = None

    for line in text.split("\n"):
        line_lower = line.lower().strip()

        for section, pattern in SECTION_PATTERNS.items():
            if re.search(pattern, line_lower):
                current_section = section
                break

        if current_section and line.strip():
            sections[current_section] += line + "\n"

    return sections

'''

file = "C:\\Users\\biele\\Desktop\\Cours\\SousWindowsRodolphe\\LLM\\PROJECT\\DRAFT\\DATA\\offre.txt"
with open(file, "r", encoding="utf-8") as f:
    text = f.read() 
sections = extract_sections(text)
for section, content in sections.items():
    print(f"--- {section.upper()} ---")
    print(content[:500])  # Print first 500 characters of each section
    print() 

'''








# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\structuring\llm_client.py

# llm_client.py

import ollama

class OllamaClient:
    def __init__(self, model="mistral"):
        self.model = model

    def generate(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]


'''







# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\matching\similarity.py
import numpy as np


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    if vec1 is None or vec2 is None:
        return 0.0
    return float(np.dot(vec1, vec2))





C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\matching\scorer.py

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








# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\matching\multi_job_matching.py

# multi_job_matching.py

from matching.scorer import compute_score

def match_cv_to_jobs(cv_embeddings, jobs_embeddings):
    rankings = []

    for job_id, job_emb in jobs_embeddings.items():
        scores = compute_score(cv_embeddings, job_emb)

        rankings.append({
            "job_id": job_id,
            "score": scores["total"],
            "details": scores
        })

    rankings.sort(key=lambda x: x["score"], reverse=True)
    return rankings







C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\matching\matching_pipeline.py
from matching.scorer import compute_score

def match_documents(cv_embeddings, job_embeddings):
    return compute_score(cv_embeddings, job_embeddings)






# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\LOADERS\txt_loader.py

from pathlib import Path

def load_txt(file_path: str) -> str:
    """
    Load raw text from a TXT file.

    Args:
        file_path (str): Path to the TXT file

    Returns:
        str: Raw text content
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"TXT file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    return text.strip()

'''
txt = load_txt("C:\\Users\\biele\\Desktop\\Cours\\SousWindowsRodolphe\\LLM\\project\\DRAFT\\DATA\\paris.txt")
print(txt[:10000])  # Affiche les 1000000 premiers caractères
'''






C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\LOADERS\pdf_loader.py

#pdf_loader.py

import pdfplumber
from pathlib import Path

def load_pdf(file_path: str) -> str:
    """
    Extract raw text from a PDF file.

    Args:
        file_path (str): Path to the PDF file

    Returns:
        str: Extracted raw text
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    text_pages = []

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text_pages.append(f"\n\n--- Page {i} ---\n\n {page_text}")

    return "\n".join(text_pages)

'''
# Exemple d'utilisation
pdf_text = load_pdf(r"C:\\Users\\biele\\Desktop\\Cours\\SousWindowsRodolphe\\LLM\\project\\DRAFT\\DATA\\datasetEtude2 (1).pdf")
print(pdf_text[:1000000])  # Affiche les 1000000 premiers caractères
'''






# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\LOADERS\docx_loader.py

from pathlib import Path
from docx import Document

def load_docx(file_path: str) -> str:
    """
    Extract raw text from a DOCX file.

    Args:
        file_path (str): Path to the DOCX file

    Returns:
        str: Extracted raw text
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"DOCX file not found: {file_path}")

    document = Document(file_path)

    paragraphs = []
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)

'''
#ASSOCIATION_SPORTIVE.docx
doc_loader = load_docx("C:\\Users\\biele\\Desktop\\Cours\\SousWindowsRodolphe\\LLM\\project\\DRAFT\\DATA\\ASSOCIATION_SPORTIVE.docx")
print(doc_loader)
'''





# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\llm\ollama_client.py

import ollama

class OllamaClient:
    def __init__(self, model="mistral:7b"):
        self.model = model

    def generate(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]





# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\ingestion\ingestion_pipeline.py

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from DRAFT.LOADERS.pdf_loader import load_pdf

from DRAFT.LOADERS.docx_loader import load_docx
from DRAFT.LOADERS.txt_loader import load_txt
from ingestion.cleaner import clean_text


def ingest_file(file_path: str) -> str:
    """
    Ingest a CV or job description file and return cleaned text.

    Args:
        file_path (str): Path to input file (PDF, DOCX, or TXT)

    Returns:
        str: Cleaned text ready for downstream processing
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        raw_text = load_pdf(file_path)
    elif suffix == ".docx":
        raw_text = load_docx(file_path)
    elif suffix == ".txt":
        raw_text = load_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")

    cleaned_text = clean_text(raw_text)

    return cleaned_text

'''

file = "C:\\Users\\biele\\Desktop\\Cours\\SousWindowsRodolphe\\LLM\\PROJECT\\DRAFT\\DATA\\paris.txt"
cleaned = ingest_file(file)
print(cleaned[:1000])  # Affiche les 1000000 premiers caractères nettoyés

'''





# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\ingestion\cleaner.py

import re


def clean_text(text: str) -> str:
    """
    Clean raw text extracted from CVs or job descriptions.

    Args:
        text (str): Raw extracted text

    Returns:
        str: Cleaned text
    """
    if not text:
        return ""

    # Normalize line breaks
    text = text.replace("\r", "\n")

    # Remove multiple spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove multiple newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove non-informative characters
    text = re.sub(r"[•·●■▪▶►]", "", text)

    # Strip leading/trailing spaces
    text = text.strip()

    return text

'''
# Affiche les 1000000 premiers caractères nettoyés
file = open("C:\\Users\\biele\\Desktop\\Cours\\SousWindowsRodolphe\\LLM\\project\\DRAFT\\DATA\\paris.txt", "r", encoding="utf-8", errors="ignore")
raw_text = file.read()
print(clean_text(raw_text[:1000]))  
'''










# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\explanation\prompt_builder.py

'''
def build_explanation_prompt(scores, cv_structured, job_structured):
    return f"""
You are an AI recruitment assistant.

Matching scores:
- Skills: {scores['skills']:.2f}
- Experience: {scores['experience']:.2f}
- Education: {scores['education']:.2f}
- Total match score: {scores['total']:.2f}

Candidate skills:
{', '.join(cv_structured['skills'])}

Job required skills:
{', '.join(job_structured['skills'])}

Explain in 4-6 bullet points:
- why the match is strong or weak
- what aligns well
- what is missing or could be improved
Use a neutral and professional tone.
"""



'''

def build_explanation_prompt(scores, cv_structured, job_structured):
    cv_skills = set(
        sum(cv_structured["skills"].values(), [])
    )
    job_skills = set(
        sum(job_structured["skills"].values(), [])
    )

    common = sorted(cv_skills & job_skills)
    missing = sorted(job_skills - cv_skills)

    return f"""
You are an AI recruitment assistant.

Explain the match between a candidate and a job offer.

Matching scores:
{scores}

Strongly matching skills:
{common[:10]}

Missing or weak skills:
{missing[:10]}

Instructions:
- Be concise and professional
- Base your explanation strictly on the information above
- Do not invent information

Provide:
1) Overall assessment (2 sentences)
2) Strengths (bullet points)
3) Gaps (bullet points)
4) One concrete recommendation
"""








# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\explanation\explanation_pipeline.py
from explanation.prompt_builder import build_explanation_prompt
from explanation.explainer import generate_explanation

def explain_match(scores, cv_structured, job_structured):
    prompt = build_explanation_prompt(scores, cv_structured, job_structured)
    return generate_explanation(prompt)







# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\explanation\explainer.py

# explainer.py

from llm.ollama_client import OllamaClient

llm = OllamaClient(model="mistral:7b")


def generate_explanation(prompt: str) -> str:
    return llm.generate(prompt)







# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\evaluation\recall.py
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







C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\evaluation\ndcg.py
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








# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\evaluation\model_comparison.csv

Model,Recall@10,NDCG@10,Latency (s)
MiniLM,0.2,0.706,1.5
MPNet,0.267,0.858,11.3






# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\evaluation\embedding_comparison.py
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






# C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\embedding\embedding_pipeline.py

# embedding_pipeline.py

from embedding.embedding_model import EmbeddingModel
from embedding.embedder import Embedder


def embed_structured_document(structured_doc):
    """
    Generate embeddings per semantic category.
    """
    model = EmbeddingModel()
    embedder = Embedder(model)

    embeddings = {}

    # --- Skills by category ---
    skills = structured_doc.get("skills", {})
    for category in [
        "hard_skills",
        "soft_skills",
        "tools_technologies",
        "domain_knowledge",
    ]:
        values = skills.get(category, [])
        embeddings[category] = embedder.embed_skills(values)

    # --- Experience ---
    embeddings["experience"] = embedder.embed_text(
        structured_doc.get("experience", "")
    )

    # --- Education ---
    embeddings["education"] = embedder.embed_text(
        structured_doc.get("education", "")
    )

    return embeddings






C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\embedding\embedding_model.py
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def encode(self, text):
        return self.model.encode(text)





C:\Users\biele\Desktop\Cours\SousWindowsRodolphe\LLM\project\DRAFT\embedding\embedder.py


#embedder.py
from typing import Dict, List
import numpy as np

from embedding.embedding_model import EmbeddingModel


class Embedder:
    def __init__(self, model: EmbeddingModel):
        self.model = model

    def embed_skills(self, skills: List[str]) -> np.ndarray | None:
        if not skills:
            return None
        return self.model.encode([" ".join(skills)])[0]

    def embed_text(self, text: str) -> np.ndarray | None:
        if not text:
            return None
        return self.model.encode([text])[0]

    '''def embed_document(self, structured_doc: Dict) -> Dict[str, np.ndarray | None]:
        experience_text = structured_doc.get("experience") or ""
        skills_text = " ".join(structured_doc.get("skills", [])) if structured_doc.get("skills") else ""

        combined_experience = f"{experience_text} {skills_text}".strip()


        return {
            "skills": self.embed_skills(structured_doc.get("skills", [])),
            "experience": self.embed_text(combined_experience),
            "education": self.embed_text(structured_doc.get("education", "")),
        }'''

    def embed_document(self, structured_doc):
        return {
            "full_text": self.embed_text(structured_doc.get("raw_text", ""))
        }





