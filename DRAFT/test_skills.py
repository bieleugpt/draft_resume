from ingestion import ingest_file
from structuring.skill_extractor_2 import SkillExtractor
from llm.ollama_client import OllamaClient
from pathlib import Path

# Init LLM
llm = OllamaClient(model="mistral:7b")
skill_extractor = SkillExtractor(llm)

# Charger un vrai texte
BASE_DIR = Path(__file__).parent
cv_path = BASE_DIR / "DATA" / "CV.pdf"

text = ingest_file(cv_path)

print("========== TEXTE ==========")
print(text[:1000])

skills = skill_extractor.extract(text)

print("\n========== SKILLS ==========")
print(skills)
