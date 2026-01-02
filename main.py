#main.py



''''
from ingestion import ingest_file
from structuring import structure_document
from embedding import embed_structured_document

from pathlib import Path

if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent
    file_path = BASE_DIR / "DATA" / "offre.txt"
    cv_path = BASE_DIR / "DATA" / "CV.pdf"
    text = ingest_file(file_path)
    cv_text = ingest_file(cv_path)
    structured = structure_document(text)
    cv_structured = structure_document(cv_text)
    embeddings = embed_structured_document(structured)
    cv_embeddings = embed_structured_document(cv_structured)
    # embeddings.update({f"cv_{k}": v for k, v in cv_embeddings.items()})

    print("\n___________________________")
    print("Embeddings generated:")
    print("---------------------------")
    for key, value in embeddings.items():
        print(key, None if value is None else value.shape)





from matching import match_documents

# test simple CV = offre (pour validation)
scores = match_documents(embeddings, cv_embeddings)

print("\n___________________________")
print("Matching scores:")
print("---------------------------")
for k, v in scores.items():
    print(k, round(v, 3))





from explanation import explain_match

explanation = explain_match(scores, cv_structured, structured)

print("\n___________________________")
print("AI Explanation:")
print("---------------------------")
print(explanation)


'''








'''
from ingestion import ingest_file
from structuring import structure_document
from embedding import embed_structured_document
from matching import match_documents
from explanation import explain_match

from pathlib import Path



import random
import numpy as np
import torch

random.seed(42)
np.random.seed(42)
torch.manual_seed(42)


def run_matching(cv_path, job_path):
    # 1. Ingestion
    cv_text = ingest_file(cv_path)
    job_text = ingest_file(job_path)

    # 2. Structuration
    cv_structured = structure_document(cv_text, doc_type="cv")
    job_structured = structure_document(job_text, doc_type="job")

    # 3. Embeddings
    cv_embeddings = embed_structured_document(cv_structured)
    job_embeddings = embed_structured_document(job_structured)

    #---------------------------------------
    # Phase intermédiaire 
    EXPECTED_KEYS = [
        "hard_skills",
        "soft_skills",
        "tools_technologies",
        "domain_knowledge",
        "experience",
        "education"
    ]

    for key in EXPECTED_KEYS:
        job_embeddings.setdefault(key, None)
        cv_embeddings.setdefault(key, None)

    #------------------------------------------

    # 4. Matching
    scores = match_documents(job_embeddings, cv_embeddings)

    # 5. Explication IA
    explanation = explain_match(scores, cv_structured, job_structured)

    return {
        "scores": scores,
        "explanation": explanation
    }


if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent

    # Paths
    job_path = BASE_DIR / "DATA" / "offre.txt"
    cv_path = BASE_DIR / "DATA" / "CV.pdf"

    # Ingestion
    job_text = ingest_file(job_path)
    cv_text = ingest_file(cv_path)

    # Structuring (⚠️ doc_type obligatoire)
    job_structured = structure_document(job_text, doc_type="job")
    cv_structured = structure_document(cv_text, doc_type="cv")

    # Embeddings
    job_embeddings = embed_structured_document(job_structured)
    cv_embeddings = embed_structured_document(cv_structured)

    print("\n___________________________")
    print("Embeddings generated:")
    print("---------------------------")
    for key, value in job_embeddings.items():
        print(key, None if value is None else value.shape)

    # Matching
    scores = match_documents(job_embeddings, cv_embeddings)

    print("\n___________________________")
    print("Matching scores:")
    print("---------------------------")
    for k, v in scores.items():
        print(k, round(v, 3))

    # Explanation
    explanation = explain_match(scores, cv_structured, job_structured)

    print("\n___________________________")
    print("AI Explanation:")
    print("---------------------------")
    print(explanation)

    '''























''' # V_Actuelle 

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

    '''




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
