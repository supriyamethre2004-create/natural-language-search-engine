import fitz
from pathlib import Path


def extract_text_from_pdf(pdf_path):
    """Extract text from every page of a PDF."""

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text()

        pages.append({
            "page": page_number,
            "text": text
        })

    document.close()

    return pages


if __name__ == "__main__":

    pdf_path = "data/raw/Attention Is All You Need PDF.pdf"

    pages = extract_text_from_pdf(pdf_path)

    print(f"Total pages: {len(pages)}")

    print("\n--- First page ---\n")
    print(pages[0]["text"][:2000])