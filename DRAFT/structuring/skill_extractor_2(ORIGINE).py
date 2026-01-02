'''
(PROMPT_1)
You are an expert HR analyst.

Your task is to extract professional skills from the following document.
The document can belong to any sector (IT, finance, marketing, healthcare, law, education, etc.).

Instructions:
- Extract only real and relevant skills explicitly or implicitly mentioned.
- Do NOT invent skills.
- Group skills into meaningful categories.
- Be concise and precise.

Return the result strictly in valid JSON with this structure:

{{
  "hard_skills": [],
  "soft_skills": [],
  "tools_technologies": [],
  "domain_knowledge": []
}}

Document:
\"\"\"
{text}
\"\"\"

'''

# skill_extractor_2.py

import json
import re
from typing import Dict, List


class SkillExtractor:
    def __init__(self, llm_client):
        self.llm = llm_client

    def extract(self, text: str) -> Dict[str, List[str]]:
        if not text.strip():
            return {
                "hard_skills": [],
                "soft_skills": [],
                "tools_technologies": [],
                "domain_knowledge": []
            }

        prompt = self._build_prompt(text)
        response = self.llm.generate(prompt)

        json_text = self._extract_json(response)

        try:
            skills = json.loads(json_text)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse JSON.\nExtracted JSON:\n{json_text}\n\nFull response:\n{response}"
            ) from e

        return self._clean_output(skills)

    def _extract_json(self, text: str) -> str:
        """
        Extract the first JSON object found in the LLM response.
        """
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError(
                f"No JSON object found in LLM response:\n{text}"
            )
        return match.group(0)

    def _build_prompt(self, text: str) -> str:
        return f"""
You are an expert HR analyst.

Your task is to extract professional skills from the following document.
The document can belong to any sector (IT, finance, marketing, healthcare, law, education, etc.).

Instructions:
- Extract only real and relevant skills explicitly or implicitly mentioned.
- Do NOT invent skills.
- Group skills into meaningful categories.
- Be concise and precise.

Return the result strictly in valid JSON with this structure:

{{
  "hard_skills": [],
  "soft_skills": [],
  "tools_technologies": [],
  "domain_knowledge": []
}}

Document:
\"\"\"
{text}
\"\"\"
"""

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
                    set(v.strip() for v in values if isinstance(v, str) and v.strip())
                )
            else:
                cleaned[key] = []
        return cleaned
