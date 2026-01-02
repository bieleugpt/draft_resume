from pathlib import Path

def list_pdfs(directory: str):
    return sorted([
        p for p in Path(directory).iterdir()
        if p.suffix.lower() == ".pdf"
    ])
