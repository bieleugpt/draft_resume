

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from DRAFT.LOADERS.pdf_loader import load_pdf

from DRAFT.LOADERS.docx_loader import load_docx
from DRAFT.LOADERS.txt_loader import load_txt
from ingestion.cleaner import clean_text


def ingest_file(file_path: str) -> str:
    """
    Ingest a CV or job description file and return cleaned text.

    Args:
        file_path (str): Path to input file (PDF, DOCX, or TXT)

    Returns:
        str: Cleaned text ready for downstream processing
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        raw_text = load_pdf(file_path)
    elif suffix == ".docx":
        raw_text = load_docx(file_path)
    elif suffix == ".txt":
        raw_text = load_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")

    cleaned_text = clean_text(raw_text)

    return cleaned_text

'''

file = "C:\\Users\\biele\\Desktop\\Cours\\SousWindowsRodolphe\\LLM\\PROJECT\\DRAFT\\DATA\\paris.txt"
cleaned = ingest_file(file)
print(cleaned[:1000])  # Affiche les 1000000 premiers caractères nettoyés

'''














