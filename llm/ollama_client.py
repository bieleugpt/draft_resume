'''

import ollama


class OllamaClient:
    def __init__(self, model="llama3:8b"):
        self.model = model

    def generate(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]

'''






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


