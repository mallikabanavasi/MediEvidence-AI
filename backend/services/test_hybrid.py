from backend.services.hybrid_retrieval import hybrid_retriever


query = "What are the treatment options for hypertension?"

results = hybrid_retriever.search(
    query,
    limit=5
)

print()
print("Hybrid Retrieval Results")
print("=" * 60)

for index, result in enumerate(
    results,
    start=1
):

    print()
    print(f"Result {index}")
    print(f"Chunk ID: {result['chunk_id']}")
    print(
        f"Hybrid Score: "
        f"{result['hybrid_score']:.4f}"
    )
    print(
        f"Text: "
        f"{result['text'][:300]}..."
    )