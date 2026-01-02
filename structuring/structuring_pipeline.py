'''

# structuring_pipeline.py

from typing import Dict

from structuring.section_extractor import extract_sections
from structuring.skill_extractor import extract_skills

from structuring.skill_extractor_2 import SkillExtractor

#llm = OllamaClient()


def structure_document(text: str) -> Dict:
    """
    Structure a CV or job description into semantic components.
    """
    sections = extract_sections(text)

    # 1. Try extracting skills from the SKILLS section
    skills = extract_skills(sections.get("skills", ""))
    #skill_extractor = SkillExtractor(llm)
    #skills = skill_extractor.extract(sections.get("skills", ""))

    # 2. Fallback: extract skills from EXPERIENCE if needed
    if not skills:
        skills = extract_skills(sections.get("experience", ""))

    return {
        "skills": skills,
        "experience": sections.get("experience", "").strip(),
        "education": sections.get("education", "").strip(),
        "raw_text": text
    }

'''

# structuring_pipeline.py

'''
from typing import Dict

from structuring.section_extractor import extract_sections
from structuring.skill_extractor_2 import SkillExtractor
from llm.ollama_client import OllamaClient


llm = OllamaClient()


def structure_document(text: str) -> Dict:
    """
    Structure a CV or job description into semantic components.
    """
    sections = extract_sections(text)

    skill_extractor = SkillExtractor(llm)

    skills_text = sections.get("skills", "").strip()
    experience_text = sections.get("experience", "").strip()

    # 1. Choose the best text source for skill extraction
    if skills_text:
        extraction_source = skills_text
    else:
        extraction_source = experience_text

    skills = skill_extractor.extract(extraction_source)

    return {
        "skills": skills,
        "experience": experience_text,
        "education": sections.get("education", "").strip(),
        "raw_text": text
    }
'''

'''

from embedding.embedding_model import EmbeddingModel
from embedding.embedder import Embedder


def embed_structured_document(structured_doc):
    model = EmbeddingModel()
    embedder = Embedder(model)

    embeddings = {}

    # 1. Skills by category
    skills = structured_doc.get("skills", {})
    for category, items in skills.items():
        if items:
            text = ", ".join(items)
            embeddings[category] = embedder.embed(text)
        else:
            embeddings[category] = None

    # 2. Experience & education
    embeddings["experience"] = embedder.embed(
        structured_doc.get("experience", "")
    )
    embeddings["education"] = embedder.embed(
        structured_doc.get("education", "")
    )

    return embeddings
'''

'''

# structuring_pipeline.py

from typing import Dict

from structuring.section_extractor import extract_sections
from structuring.skill_extractor_2 import SkillExtractor
from llm.ollama_client import OllamaClient


llm = OllamaClient(model="llama3:8b")


def structure_document(text: str) -> Dict:
    """
    Structure a CV or job description into semantic components.
    """
    sections = extract_sections(text)

    skill_extractor = SkillExtractor(llm)

    skills_text = sections.get("skills", "").strip()
    experience_text = sections.get("experience", "").strip()

    if skills_text:
        extraction_source = skills_text
    else:
        extraction_source = experience_text

    skills = skill_extractor.extract(extraction_source)

    # Ensure all skill categories exist
    normalized_skills = {
        "hard_skills": skills.get("hard_skills", []),
        "soft_skills": skills.get("soft_skills", []),
        "tools_technologies": skills.get("tools_technologies", []),
        "domain_knowledge": skills.get("domain_knowledge", []),
    }


    return {
        "skills": normalized_skills,
        "experience": experience_text,
        "education": sections.get("education", "").strip(),
        "raw_text": text
    }

'''


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




