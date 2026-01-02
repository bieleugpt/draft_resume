
from pathlib import Path
from docx import Document


def load_docx(file_path: str) -> str:
    """
    Extract raw text from a DOCX file.

    Args:
        file_path (str): Path to the DOCX file

    Returns:
        str: Extracted raw text
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"DOCX file not found: {file_path}")

    document = Document(file_path)

    paragraphs = []
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)

'''
#ASSOCIATION_SPORTIVE.docx
doc_loader = load_docx("C:\\Users\\biele\\Desktop\\Cours\\SousWindowsRodolphe\\LLM\\project\\DRAFT\\DATA\\ASSOCIATION_SPORTIVE.docx")
print(doc_loader)
'''