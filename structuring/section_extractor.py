import re
from typing import Dict



SECTION_PATTERNS = {
    "skills": r"(skills|competencies|technical skills|Vous maitrisez)",
    "experience": r"(experience|work experience|professional experience|le profil recherché|profil recherché|votre profil|Vous possédez|vous avez|une expérience)",
    "education": r"(education|academic background|studies|titulaire|diplômé de|diplômée de)",
}


def extract_sections(text: str) -> Dict[str, str]:
    """
    Extract main sections from a CV or job description.

    Args:
        text (str): Cleaned input text

    Returns:
        Dict[str, str]: Sections mapped to their content
    """
    sections = {key: "" for key in SECTION_PATTERNS}
    current_section = None

    for line in text.split("\n"):
        line_lower = line.lower().strip()

        for section, pattern in SECTION_PATTERNS.items():
            if re.search(pattern, line_lower):
                current_section = section
                break

        if current_section and line.strip():
            sections[current_section] += line + "\n"

    return sections

'''

file = "C:\\Users\\biele\\Desktop\\Cours\\SousWindowsRodolphe\\LLM\\PROJECT\\DRAFT\\DATA\\offre.txt"
with open(file, "r", encoding="utf-8") as f:
    text = f.read() 
sections = extract_sections(text)
for section, content in sections.items():
    print(f"--- {section.upper()} ---")
    print(content[:500])  # Print first 500 characters of each section
    print() 

'''