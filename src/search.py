import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi


EMBEDDINGS_FILE = Path("data/processed/embeddings.json")


def load_data():
    """Load chunks and their embeddings."""

    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def normalize_scores(scores):
    """Normalize scores between 0 and 1."""

    minimum = scores.min()
    maximum = scores.max()

    if maximum == minimum:
        return scores

    return (scores - minimum) / (maximum - minimum)


def search(query, top_k=5):
    """Find relevant chunks using semantic search with BM25 support."""

    print("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    data = load_data()

    # -----------------------------
    # Semantic Search
    # -----------------------------

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    document_embeddings = [
        item["embedding"]
        for item in data
    ]

    semantic_scores = cosine_similarity(
        query_embedding,
        document_embeddings
    )[0]

    # -----------------------------
    # BM25 Keyword Search
    # -----------------------------

    tokenized_documents = [
        item["text"].lower().split()
        for item in data
    ]

    bm25 = BM25Okapi(tokenized_documents)

    tokenized_query = query.lower().split()

    bm25_scores = bm25.get_scores(tokenized_query)

    normalized_bm25 = normalize_scores(bm25_scores)

    # -----------------------------
    # Hybrid Ranking
    # -----------------------------

    semantic_weight = 0.95
    bm25_weight = 0.05

    combined_scores = (
        semantic_weight * semantic_scores
        + bm25_weight * normalized_bm25
    )

    # -----------------------------
    # Rank Results
    # -----------------------------

    ranked_indices = combined_scores.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:

        result = data[index].copy()

        result["semantic_score"] = float(
            semantic_scores[index]
        )

        result["bm25_score"] = float(
            normalized_bm25[index]
        )

        result["combined_score"] = float(
            combined_scores[index]
        )

        results.append(result)

    return results


if __name__ == "__main__":

    query = input("\nEnter your search query: ")

    results = search(query)

    print("\n==============================")
    print("HYBRID SEARCH RESULTS")
    print("==============================")

    for rank, result in enumerate(results, start=1):

        print(f"\nResult {rank}")

        print(f"Source: {result['source']}")

        print(f"Page: {result['page']}")

        print(
            f"Semantic Score: "
            f"{result['semantic_score']:.4f}"
        )

        print(
            f"BM25 Score: "
            f"{result['bm25_score']:.4f}"
        )

        print(
            f"Combined Score: "
            f"{result['combined_score']:.4f}"
        )

        print("\nText:")

        print(result["text"][:500])

        print("------------------------------")