import json
import re
from pathlib import Path

from rank_bm25 import BM25Okapi


EMBEDDINGS_FILE = Path(
    "data/knowledge_base/processed/embeddings/embeddings.json"
)


class BM25Service:

    def __init__(self):

        print("Loading BM25 search index...")

        with open(
            EMBEDDINGS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            self.documents = json.load(file)

        self.texts = [
            document["text"]
            for document in self.documents
        ]

        self.tokenized_documents = [
            self.tokenize(text)
            for text in self.texts
        ]

        self.bm25 = BM25Okapi(
            self.tokenized_documents
        )

        print(
            f"BM25 index loaded with "
            f"{len(self.documents)} documents."
        )

    @staticmethod
    def tokenize(text):

        return re.findall(
            r"\b\w+\b",
            text.lower()
        )

    def search(
        self,
        query,
        limit=5
    ):

        query_tokens = self.tokenize(query)

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked_indexes = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True
        )

        results = []

        for index in ranked_indexes[:limit]:

            results.append(
                {
                    "chunk_id": self.documents[index]["chunk_id"],
                    "text": self.documents[index]["text"],
                    "score": float(scores[index]),
                }
            )

        return results


bm25_service = BM25Service()