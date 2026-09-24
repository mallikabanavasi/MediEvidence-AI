from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class Reranker:

    def __init__(self):

        print("Loading Cross-Encoder model...")

        self.model = CrossEncoder(
            MODEL_NAME
        )

        print(
            "Cross-Encoder model loaded successfully."
        )

    def rerank(
        self,
        query,
        results,
        limit=5
    ):

        if not results:
            return []

        pairs = [
            [
                query,
                result["text"]
            ]
            for result in results
        ]

        scores = self.model.predict(
            pairs
        )

        reranked_results = []

        for result, score in zip(
            results,
            scores
        ):

            updated_result = result.copy()

            updated_result[
                "reranker_score"
            ] = float(score)

            reranked_results.append(
                updated_result
            )

        reranked_results.sort(
            key=lambda item: item[
                "reranker_score"
            ],
            reverse=True
        )

        return reranked_results[:limit]


reranker = Reranker()