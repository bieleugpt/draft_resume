
'''
# llm_client.py

import ollama


class OllamaClient:
    def __init__(self, model="llama3"):
        self.model = model

    def generate(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]


'''


















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