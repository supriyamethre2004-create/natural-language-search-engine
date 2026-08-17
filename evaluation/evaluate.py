import json
import sys
from pathlib import Path

# Allow Python to import search.py from src/
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from search import search


QUERIES_FILE = Path("evaluation/queries.json")


def load_queries():
    """Load evaluation queries and their relevant pages."""

    with open(QUERIES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def unique_pages(results):
    """Remove duplicate chunks from the same PDF page."""

    seen = set()
    unique_results = []

    for result in results:
        page_id = (
            result["source"],
            result["page"]
        )

        if page_id not in seen:
            seen.add(page_id)
            unique_results.append(result)

    return unique_results


def is_relevant(result, relevant_pages):
    """Check whether a result matches a relevant page."""

    for page in relevant_pages:

        if (
            result["source"] == page["source"]
            and result["page"] == page["page"]
        ):
            return True

    return False


def calculate_recall_at_k(results, relevant_pages, k):
    """Calculate Recall@K using unique PDF pages."""

    results = unique_pages(results[:k])

    relevant_found = sum(
        is_relevant(result, relevant_pages)
        for result in results
    )

    return min(
        relevant_found / len(relevant_pages),
        1.0
    )


def calculate_precision_at_k(results, relevant_pages, k):
    """Calculate Precision@K using unique PDF pages."""

    results = unique_pages(results[:k])

    if not results:
        return 0.0

    relevant_found = sum(
        is_relevant(result, relevant_pages)
        for result in results
    )

    return relevant_found / len(results)


def main():

    queries = load_queries()

    recall_scores = []
    precision_scores = []

    print("\n==============================")
    print("SEARCH ENGINE EVALUATION")
    print("==============================")

    for item in queries:

        query = item["query"]
        relevant_pages = item["relevant_pages"]

        print(f"\nQuery: {query}")

        results = search(query, top_k=5)

        recall = calculate_recall_at_k(
            results,
            relevant_pages,
            k=5
        )

        precision = calculate_precision_at_k(
            results,
            relevant_pages,
            k=5
        )

        recall_scores.append(recall)
        precision_scores.append(precision)

        print(f"Recall@5: {recall:.2f}")
        print(f"Precision@5: {precision:.2f}")

    average_recall = sum(recall_scores) / len(recall_scores)
    average_precision = sum(precision_scores) / len(precision_scores)

    print("\n==============================")
    print("OVERALL RESULTS")
    print("==============================")

    print(f"Average Recall@5: {average_recall:.2f}")
    print(f"Average Precision@5: {average_precision:.2f}")


if __name__ == "__main__":
    main()