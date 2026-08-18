import re


def clean_text(text):
    """
    Clean extracted PDF text before chunking.
    """

    # Remove common PDF/tokenizer artifacts
    text = re.sub(r"<EOS>|<pad>", " ", text)

    # Join words broken by PDF line wrapping, e.g.:
    # "atten-\ntion" -> "attention"
    text = re.sub(r"-\s*\n\s*", "", text)

    # Replace newlines with spaces
    text = re.sub(r"\s+", " ", text)

    # Remove spaces before punctuation
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)

    return text.strip()


def split_into_sentences(text):
    """
    Split cleaned text into sentences.
    """

    sentences = re.split(r"(?<=[.!?])\s+", text)

    return [sentence.strip() for sentence in sentences if sentence.strip()]


def chunk_pages(pages, chunk_size=600, overlap=100):
    """
    Split extracted PDF text into overlapping, sentence-aware chunks.
    """

    chunks = []

    for page in pages:

        text = clean_text(page["text"])
        page_number = page["page"]

        # Ignore empty or extremely short pages
        if len(text) < 100:
            continue

        sentences = split_into_sentences(text)

        current_chunk = ""

        for sentence in sentences:

            # If adding the next sentence stays within the target size
            if len(current_chunk) + len(sentence) + 1 <= chunk_size:

                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence

            else:

                # Save current chunk
                if len(current_chunk) >= 100:
                    chunks.append({
                        "page": page_number,
                        "text": current_chunk
                    })

                # Create overlap using the end of the previous chunk
                overlap_text = current_chunk[-overlap:] if current_chunk else ""

                current_chunk = overlap_text + " " + sentence

        # Save final chunk
        if len(current_chunk.strip()) >= 100:
            chunks.append({
                "page": page_number,
                "text": current_chunk.strip()
            })

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