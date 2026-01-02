

import re


def clean_text(text: str) -> str:
    """
    Clean raw text extracted from CVs or job descriptions.

    Args:
        text (str): Raw extracted text

    Returns:
        str: Cleaned text
    """
    if not text:
        return ""

    # Normalize line breaks
    text = text.replace("\r", "\n")

    # Remove multiple spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove multiple newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove non-informative characters
    text = re.sub(r"[•·●■▪▶►]", "", text)

    # Strip leading/trailing spaces
    text = text.strip()

    return text

'''
# Affiche les 1000000 premiers caractères nettoyés
file = open("C:\\Users\\biele\\Desktop\\Cours\\SousWindowsRodolphe\\LLM\\project\\DRAFT\\DATA\\paris.txt", "r", encoding="utf-8", errors="ignore")
raw_text = file.read()
print(clean_text(raw_text[:1000]))  
'''













