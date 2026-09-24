from backend.services.bm25_service import bm25_service


query = "hypertension treatment"

results = bm25_service.search(
    query,
    limit=5
)

print()
print("BM25 Search Results")
print("=" * 60)

for index, result in enumerate(results, start=1):

    print()
    print(f"Result {index}")
    print(f"Chunk ID: {result['chunk_id']}")
    print(f"Score: {result['score']:.4f}")
    print(f"Text: {result['text'][:300]}...")