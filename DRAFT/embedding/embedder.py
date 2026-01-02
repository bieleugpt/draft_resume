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

    def embed_document(self, structured_doc: Dict) -> Dict[str, np.ndarray | None]:
        combined_experience = (
            structured_doc.get("experience", "") +
            " " +
            " ".join(structured_doc.get("skills", []))
        )

        return {
            "skills": self.embed_skills(structured_doc.get("skills", [])),
            "experience": self.embed_text(combined_experience),
            "education": self.embed_text(structured_doc.get("education", "")),
        }

