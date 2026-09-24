from backend.services.evidence_retrieval import evidence_retriever


query = "What are the treatment options for hypertension?"


results = evidence_retriever.search(
    query,
    retrieval_limit=10,
    final_limit=5
)


print()
print("Evidence Retrieval Results")
print("=" * 60)


for index, result in enumerate(
    results,
    start=1
):

    print()
    print(f"Evidence {index}")
    print(f"Chunk ID: {result['chunk_id']}")
    print(
        f"Reranker Score: "
        f"{result['reranker_score']:.4f}"
    )
    print(
        f"Text: "
        f"{result['text'][:400]}..."
    )