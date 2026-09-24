class RAGContextBuilder:

    def build_context(
        self,
        query: str,
        evidence_results: list
    ):

        context_parts = []

        context_parts.append(
            f"Clinical Question:\n{query}\n"
        )

        context_parts.append(
            "Retrieved Medical Evidence:\n"
        )

        for index, result in enumerate(
            evidence_results,
            start=1
        ):

            context_parts.append(
                f"Evidence {index}\n"
                f"Chunk ID: {result['chunk_id']}\n"
                f"Relevance Score: "
                f"{result['reranker_score']:.4f}\n"
                f"Text:\n"
                f"{result['text']}\n"
                f"{'-' * 50}\n"
            )

        context_parts.append(
            "Instruction:\n"
            "Use only the retrieved evidence "
            "to support the response. "
            "Do not invent medical facts."
        )

        return "\n".join(context_parts)


rag_context_builder = RAGContextBuilder()