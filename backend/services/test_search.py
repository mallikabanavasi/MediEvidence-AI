from backend.services.embedding_service import embedding_service
from backend.services.vector_store import vector_store


query = "How can a clinical decision support tool help with COVID-19 treatment?"

print("Generating query embedding...")

embedding = embedding_service.generate_embedding(query)

print("Searching Qdrant...")

results = vector_store.search(
    embedding,
    limit=3
)

print("\nTop results:\n")

for result in results:

    print(
        f"Score: {result.score:.4f}"
    )

    print(
        f"Chunk: {result.payload['chunk_id']}"
    )

    print(
        result.payload["text"][:300]
    )

    print("-" * 60)