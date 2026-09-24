from backend.services.embedding_service import embedding_service
from backend.services.vector_store import vector_store
from backend.services.bm25_service import bm25_service


class HybridRetriever:

    def search(
        self,
        query: str,
        limit: int = 5
    ):

        # -----------------------------
        # 1. Semantic search
        # -----------------------------

        query_embedding = (
            embedding_service.generate_embedding(
                query
            )
        )

        semantic_results = vector_store.search(
            query_embedding,
            limit=limit
        )

        # -----------------------------
        # 2. BM25 keyword search
        # -----------------------------

        keyword_results = bm25_service.search(
            query,
            limit=limit
        )

        # -----------------------------
        # 3. Reciprocal Rank Fusion
        # -----------------------------

        rrf_scores = {}

        documents = {}

        k = 60

        # Semantic ranking

        for rank, result in enumerate(
            semantic_results,
            start=1
        ):

            chunk_id = result.payload["chunk_id"]

            documents[chunk_id] = {
                "chunk_id": chunk_id,
                "text": result.payload["text"],
            }

            rrf_scores[chunk_id] = (
                rrf_scores.get(chunk_id, 0)
                + 1 / (k + rank)
            )

        # BM25 ranking

        for rank, result in enumerate(
            keyword_results,
            start=1
        ):

            chunk_id = result["chunk_id"]

            if chunk_id not in documents:

                documents[chunk_id] = {
                    "chunk_id": chunk_id,
                    "text": result["text"],
                }

            rrf_scores[chunk_id] = (
                rrf_scores.get(chunk_id, 0)
                + 1 / (k + rank)
            )

        # -----------------------------
        # 4. Create final ranking
        # -----------------------------

        ranked_chunks = sorted(
            rrf_scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        results = []

        for chunk_id, score in ranked_chunks[:limit]:

            results.append(
                {
                    "chunk_id": chunk_id,
                    "text": documents[chunk_id]["text"],
                    "hybrid_score": score,
                }
            )

        return results


hybrid_retriever = HybridRetriever()