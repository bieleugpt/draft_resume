from typing import List


KNOWN_SKILLS = [
    "python", "sql", "java", "machine learning", "deep learning",
    "data analysis", "docker", "kubernetes", "aws", "gcp", "azure"
]


def extract_skills(text: str) -> List[str]:
    """
    Extract explicit skills from text using keyword matching.

    Args:
        text (str): Input text

    Returns:
        List[str]: Detected skills
    """
    text_lower = text.lower()
    skills_found = []

    for skill in KNOWN_SKILLS:
        if skill in text_lower:
            skills_found.append(skill)

    return list(set(skills_found))

'''

file = "C:\\Users\\biele\\Desktop\\Cours\\SousWindowsRodolphe\\LLM\\PROJECT\\DRAFT\\DATA\\offre.txt"
with open(file, "r", encoding="utf-8") as f:
    text = f.read() 
skills = extract_skills(text)
for skill in skills:
    print(f"--- {skill.upper()} ---")
    print(skill[:500])  # Print first 500 characters of each skill
    print() 

'''