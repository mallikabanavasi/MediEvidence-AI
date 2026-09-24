from backend.services.embedding_service import embedding_service
from backend.services.vector_store import vector_store


query = "What is hypertension?"

query_embedding = embedding_service.generate_embedding(
    query
)

results = vector_store.search(
    query_embedding,
    limit=5
)

print()
print("Qdrant Search Results")
print("=" * 60)

for index, result in enumerate(results, start=1):

    print()
    print(f"Result {index}")
    print(f"Chunk ID: {result.payload['chunk_id']}")
    print(f"Score: {result.score:.4f}")
    print(f"Text: {result.payload['text'][:300]}...")