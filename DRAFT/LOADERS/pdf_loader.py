
import pdfplumber
from pathlib import Path

def load_pdf(file_path: str) -> str:
    """
    Extract raw text from a PDF file.

    Args:
        file_path (str): Path to the PDF file

    Returns:
        str: Extracted raw text
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    text_pages = []

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text_pages.append(f"\n\n--- Page {i} ---\n\n {page_text}")

    return "\n".join(text_pages)

'''
# Exemple d'utilisation
pdf_text = load_pdf(r"C:\\Users\\biele\\Desktop\\Cours\\SousWindowsRodolphe\\LLM\\project\\DRAFT\\DATA\\datasetEtude2 (1).pdf")
print(pdf_text[:1000000])  # Affiche les 1000000 premiers caractères
'''

