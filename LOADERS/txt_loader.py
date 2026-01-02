

from pathlib import Path


def load_txt(file_path: str) -> str:
    """
    Load raw text from a TXT file.

    Args:
        file_path (str): Path to the TXT file

    Returns:
        str: Raw text content
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"TXT file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    return text.strip()

'''
txt = load_txt("C:\\Users\\biele\\Desktop\\Cours\\SousWindowsRodolphe\\LLM\\project\\DRAFT\\DATA\\paris.txt")
print(txt[:10000])  # Affiche les 1000000 premiers caractères
'''