import re
from typing import Dict


# =========================
# Section patterns (FR + EN)
# =========================
SECTION_PATTERNS = {
    "skills": [
        r"comp[eé]tences?",
        r"comp[eé]tences?\s+techniques?",
        r"soft\s*skills?",
        r"hard\s*skills?",
        r"programmation",
        r"outils",
        r"technologies?",
        r"profil",
    ],
    "experience": [
        r"exp[eé]rience",
        r"exp[eé]rience\s+professionnelle",
        r"parcours\s+professionnel",
        r"emploi",
        r"poste",
    ],
    "education": [
        r"formation",
        r"[eé]ducation",
        r"dipl[oô]me",
        r"parcours\s+acad[eé]mique",
        r"[eé]tudes",
    ],
}


# =========================
# Normalisation texte PDF
# =========================
def normalize_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


# =========================
# Section extraction
# =========================
def extract_sections(text: str) -> Dict[str, str]:
    """
    Extraction robuste des sections à partir d'un texte PDF bruité.
    Ne dépend pas d'une mise en page parfaite.
    """

    text = normalize_text(text)
    lower_text = text.lower()

    sections = {
        "skills": "",
        "experience": "",
        "education": "",
    }

    # -------------------------
    # Trouver toutes les ancres
    # -------------------------
    anchors = []

    for section, patterns in SECTION_PATTERNS.items():
        for pattern in patterns:
            for match in re.finditer(pattern, lower_text, re.IGNORECASE):
                anchors.append(
                    {
                        "section": section,
                        "start": match.start(),
                    }
                )

    # Aucun titre détecté
    if not anchors:
        return sections

    # Trier par position dans le texte
    anchors = sorted(anchors, key=lambda x: x["start"])

    # -------------------------
    # Découpage par zones
    # -------------------------
    for i, anchor in enumerate(anchors):
        section = anchor["section"]
        start = anchor["start"]

        end = (
            anchors[i + 1]["start"]
            if i + 1 < len(anchors)
            else len(text)
        )

        chunk = text[start:end].strip()

        # On concatène si plusieurs ancres pour la même section
        sections[section] += " " + chunk

    # Nettoyage final
    for key in sections:
        sections[key] = sections[key].strip()

    return sections
