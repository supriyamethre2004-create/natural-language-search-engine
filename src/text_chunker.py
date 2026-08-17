import re


def clean_text(text):
    """
    Clean extracted PDF text before chunking.
    """

    # Remove common PDF/tokenizer artifacts
    text = re.sub(r"<EOS>|<pad>", " ", text)

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove spaces before punctuation
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)

    return text.strip()


def chunk_pages(pages, chunk_size=1000, overlap=200):
    """
    Split extracted PDF text into smaller overlapping chunks.
    """

    chunks = []

    for page in pages:
        text = clean_text(page["text"])
        page_number = page["page"]

        # Ignore empty or extremely short pages
        if len(text) < 100:
            continue

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            # Ignore very short chunks
            if len(chunk_text) >= 100:
                chunks.append({
                    "page": page_number,
                    "text": chunk_text
                })

            start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    from document_loader import extract_text_from_pdf

    pdf_path = "data/raw/Attention Is All You Need PDF.pdf"

    pages = extract_text_from_pdf(pdf_path)

    chunks = chunk_pages(pages)

    print(f"Total pages: {len(pages)}")
    print(f"Total chunks: {len(chunks)}")

    print("\n--- First chunk ---\n")
    print(chunks[0]["text"])