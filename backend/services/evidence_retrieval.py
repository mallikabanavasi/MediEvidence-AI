from backend.services.hybrid_retrieval import hybrid_retriever
from backend.services.reranker import reranker


class EvidenceRetriever:

    def search(
        self,
        query: str,
        retrieval_limit: int = 10,
        final_limit: int = 5
    ):

        # Step 1: Hybrid retrieval
        hybrid_results = hybrid_retriever.search(
            query,
            limit=retrieval_limit
        )

        # Step 2: Cross-Encoder re-ranking
        reranked_results = reranker.rerank(
            query,
            hybrid_results,
            limit=final_limit
        )

        return reranked_results


evidence_retriever = EvidenceRetriever()