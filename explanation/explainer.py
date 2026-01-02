#explainer.py

'''
import ollama

def generate_explanation(prompt: str) -> str:
    response = ollama.chat(
        model="llama3:8b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]
'''

'''
# explainer.py

from llm.ollama_client import OllamaClient

llm = OllamaClient(model="llama3:8b")


def generate_explanation(prompt: str) -> str:
    return llm.generate(prompt)

    '''




# explainer.py

from llm.ollama_client import OllamaClient

llm = OllamaClient(model="mistral:7b")


def generate_explanation(prompt: str) -> str:
    return llm.generate(prompt)
