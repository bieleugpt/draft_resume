# embedding_pipeline.py
from typing import Dict
from sentence_transformers import SentenceTransformer

print("EMBEDDING FILE USED:", __file__)

_model = SentenceTransformer("all-mpnet-base-v2")


def embed_structured_document(structured_doc: Dict) -> Dict:
    embeddings = {}

    for key, value in structured_doc.items():
        if value is None:
            embeddings[key] = None
            continue

        text = str(value).strip()
        embeddings[key] = _model.encode(text) if text else None

    return embeddings
