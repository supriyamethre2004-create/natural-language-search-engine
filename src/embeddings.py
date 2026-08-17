import json
from pathlib import Path

from sentence_transformers import SentenceTransformer


INPUT_FILE = Path("data/processed/chunks.json")
OUTPUT_FILE = Path("data/processed/embeddings.json")


def create_embeddings():
    print("Loading chunks...")

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    print(f"Total chunks: {len(chunks)}")

    print("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [chunk["text"] for chunk in chunks]

    print("Creating embeddings...")

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    output = []

    for chunk, embedding in zip(chunks, embeddings):
        output.append({
            "source": chunk["source"],
            "page": chunk["page"],
            "text": chunk["text"],
            "embedding": embedding.tolist()
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(output, file)

    print("\n-----------------------------")
    print("Embedding creation completed!")
    print(f"Total embeddings: {len(embeddings)}")
    print(f"Saved to: {OUTPUT_FILE}")
    print("-----------------------------")


if __name__ == "__main__":
    create_embeddings()