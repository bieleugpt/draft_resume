# structuring_pipeline.py

from typing import Dict
import re

from structuring.section_extractor import extract_sections
from structuring.skill_extractor_2 import SkillExtractor
from llm.ollama_client import OllamaClient
from sentence_transformers import SentenceTransformer
from matching.similarity import cosine_similarity

print("STRUCTURING FILE USED:", __file__)

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
# JOB EXPERIENCE EXTRACTION
# =====================================================
def extract_job_experience(text: str) -> str:
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

    return " ".join(set(matches)) if matches else ""

# =====================================================
# JOB EDUCATION EXTRACTION
# =====================================================
def extract_job_education(text: str) -> str:
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

    return " ".join(set(matches)) if matches else ""

# =====================================================
# TOOLS & TECHNOLOGIES EXTRACTION
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
# MAIN STRUCTURING FUNCTION (FINAL, MIXTE ATS + LLM)
# =====================================================
def structure_document(text: str, doc_type: str) -> Dict:
    """
    doc_type: "cv" or "job"
    """

    sections = extract_sections(text)

    skills_text = sections.get("skills", "").strip()
    experience_text = sections.get("experience", "").strip()
    education_text = sections.get("education", "").strip()

    # 🔥 LOGIQUE MIXTE
    # CV : LLM-FIRST (ATS fallback)
    # JOB : sections + LLM
    if doc_type == "cv":
        extraction_source = skills_text if len(skills_text) > 50 else text
    else:
        extraction_source = skills_text or experience_text or text

    print("[DEBUG] extraction_source length:", len(extraction_source))

    skill_extractor = SkillExtractor(llm)
    skills = skill_extractor.extract(extraction_source)

    print("[DEBUG] skills extracted:", skills)

    hard_skills = " ".join(skills.get("hard_skills", []))
    soft_skills = " ".join(skills.get("soft_skills", []))
    domain_knowledge = " ".join(skills.get("domain_knowledge", []))

    tools_technologies = " ".join(extract_tools_technologies(text))

    if doc_type == "job":
        experience = extract_job_experience(text)
        education = extract_job_education(text)
    else:
        experience = experience_text
        education = education_text

    return {
        "hard_skills": hard_skills,
        "soft_skills": soft_skills,
        "domain_knowledge": domain_knowledge,
        "tools_technologies": tools_technologies,
        "experience": experience,
        "education": education,
        "raw_text": text,
        "full_text": text
    }
