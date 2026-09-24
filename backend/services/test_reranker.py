from backend.services.hybrid_retrieval import hybrid_retriever
from backend.services.reranker import reranker


query = "What are the treatment options for hypertension?"


hybrid_results = hybrid_retriever.search(
    query,
    limit=10
)


results = reranker.rerank(
    query,
    hybrid_results,
    limit=5
)


print()
print("Re-ranked Evidence Results")
print("=" * 60)


for index, result in enumerate(
    results,
    start=1
):

    print()
    print(f"Result {index}")
    print(f"Chunk ID: {result['chunk_id']}")
    print(
        f"Reranker Score: "
        f"{result['reranker_score']:.4f}"
    )
    print(
        f"Text: "
        f"{result['text'][:300]}..."
    )