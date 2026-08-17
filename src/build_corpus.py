from pathlib import Path
import json

from document_loader import extract_text_from_pdf
from text_chunker import chunk_pages


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")


def build_corpus():
    """Extract and chunk text from all PDFs in the raw data folder."""

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = list(RAW_DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return

    all_chunks = []

    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")

        pages = extract_text_from_pdf(pdf_file)
        chunks = chunk_pages(pages)

        for chunk in chunks:
            chunk["source"] = pdf_file.name

        all_chunks.extend(chunks)

        print(f"Pages: {len(pages)}")
        print(f"Chunks: {len(chunks)}")

    output_file = PROCESSED_DATA_DIR / "chunks.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(all_chunks, file, ensure_ascii=False, indent=2)

    print("\n-----------------------------")
    print("Corpus building completed!")
    print(f"Total PDFs: {len(pdf_files)}")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Saved to: {output_file}")
    print("-----------------------------")


if __name__ == "__main__":
    build_corpus()