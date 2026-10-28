from pathlib import Path
import pymupdf


def read_pdf(file_path: Path) -> list[dict]:
    pages = []

    with pymupdf.open(file_path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            pages.append({
                "text": text,
                "page": page_number,
                "source": file_path.name
            })

    return pages
