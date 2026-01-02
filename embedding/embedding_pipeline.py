
#embedding_pipeline.py

'''
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


from embedding.embedding_model import EmbeddingModel
from embedding.embedder import Embedder


def embed_structured_document(structured_doc):
    """
    Generate embeddings for a structured CV or job description.
    """
    model = EmbeddingModel()
    embedder = Embedder(model)

    return embedder.embed_document(structured_doc)


'''












'''
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
        if values:
            text = ", ".join(values)
            embeddings[category] = embedder.embed(text)
        else:
            embeddings[category] = None

    # --- Experience ---
    experience_text = structured_doc.get("experience", "")
    embeddings["experience"] = (
        embedder.embed(experience_text) if experience_text else None
    )

    # --- Education ---
    education_text = structured_doc.get("education", "")
    embeddings["education"] = (
        embedder.embed(education_text) if education_text else None
    )

    return embeddings
'''

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
