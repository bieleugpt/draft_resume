
'''
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        return self.model.encode(texts, normalize_embeddings=True)


        '''





'''
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self, model_name: str = "all-mpnet-base-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        return self.model.encode(texts, normalize_embeddings=True)


'''


from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def encode(self, text):
        return self.model.encode(text)
