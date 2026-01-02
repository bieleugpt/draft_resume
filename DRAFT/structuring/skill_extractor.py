

import json
import re
from typing import Dict, List


class SkillExtractor:
    def __init__(self, llm_client):
        self.llm = llm_client

    # =========================
    # Public API
    # =========================
    def extract(self, text: str) -> Dict[str, List[str]]:
        if not text.strip():
            return self._empty_skills()

        # 1️⃣ Initial extraction
        prompt = self._build_prompt(text)
        response = self.llm.generate(prompt)

        skills = self._safe_parse(response)

        # 2️⃣ Optional validation (non-blocking)
        skills = self._validate_with_llm_safe(skills)

        return self._clean_output(skills)

    # =========================
    # LLM validation (SAFE)
    # =========================
    def _validate_with_llm_safe(self, skills: Dict) -> Dict:
        prompt = f"""
You are a strict JSON validator.

You must return ONLY a valid JSON object.
No explanations. No markdown. No comments.

Schema:
{{
  "hard_skills": [string],
  "soft_skills": [string],
  "tools_technologies": [string],
  "domain_knowledge": [string]
}}

Validate and clean the following skills.
Remove irrelevant items.
Do NOT add new skills.

Input:
{json.dumps(skills)}
"""

        response = self.llm.generate(prompt)

        validated = self._safe_parse(response)

        # Fallback: if validation fails, keep original
        return validated if validated else skills

    # =========================
    # Robust JSON parsing
    # =========================
    def _safe_parse(self, text: str) -> Dict:
        # 1️⃣ Try direct JSON
        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        # 2️⃣ Try to extract JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

        # 3️⃣ Ultimate fallback
        return self._empty_skills()

    # =========================
    # Prompt
    # =========================
    def _build_prompt(self, text: str) -> str:
        return f"""
You are a strict JSON generator.

Return ONLY a valid JSON object.
Do not add explanations, comments, or markdown.

Schema:
{{
  "hard_skills": [],
  "soft_skills": [],
  "tools_technologies": [],
  "domain_knowledge": []
}}

Extract real professional skills from the following document.
Do NOT invent skills.

Document:
\"\"\"
{text}
\"\"\"
"""

    # =========================
    # Utils
    # =========================
    def _empty_skills(self) -> Dict[str, List[str]]:
        return {
            "hard_skills": [],
            "soft_skills": [],
            "tools_technologies": [],
            "domain_knowledge": []
        }

    def _clean_output(self, skills: Dict) -> Dict[str, List[str]]:
        cleaned = {}
        for key in [
            "hard_skills",
            "soft_skills",
            "tools_technologies",
            "domain_knowledge",
        ]:
            values = skills.get(key, [])
            if isinstance(values, list):
                cleaned[key] = list(
                    set(
                        v.strip()
                        for v in values
                        if isinstance(v, str) and v.strip()
                    )
                )
            else:
                cleaned[key] = []
        return cleaned
