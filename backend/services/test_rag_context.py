from backend.services.evidence_retrieval import evidence_retriever
from backend.services.rag_context import rag_context_builder


query = "What are the treatment options for hypertension?"


evidence_results = evidence_retriever.search(
    query,
    retrieval_limit=10,
    final_limit=5
)


context = rag_context_builder.build_context(
    query,
    evidence_results
)


print()
print("RAG Context")
print("=" * 60)
print()

print(context)