from pathlib import Path
import json

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)


EMBEDDINGS_FILE = Path(
    "data/knowledge_base/processed/embeddings/embeddings.json"
)

QDRANT_PATH = "data/knowledge_base/qdrant"

COLLECTION_NAME = "medical_evidence"

VECTOR_SIZE = 1024


class VectorStore:

    def __init__(self):

        print("Initializing Qdrant...")

        self.client = QdrantClient(
            path=QDRANT_PATH
        )

        self._create_collection()

        print(
            "Qdrant initialized successfully."
        )


    def _create_collection(self):

        existing_collections = (
            self.client.get_collections()
        )

        collection_names = [
            collection.name
            for collection
            in existing_collections.collections
        ]

        if COLLECTION_NAME not in collection_names:

            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )

            print(
                f"Collection created: "
                f"{COLLECTION_NAME}"
            )


    def rebuild_collection(self):

        if not EMBEDDINGS_FILE.exists():

            print(
                "Embeddings file was not found."
            )

            return


        with open(
            EMBEDDINGS_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            embeddings_data = json.load(file)


        self.client.delete_collection(
            collection_name=COLLECTION_NAME
        )

        self.client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )


        points = []

        for index, item in enumerate(
            embeddings_data
        ):

            points.append(
                PointStruct(
                    id=index + 1,
                    vector=item["embedding"],
                    payload={
                        "chunk_id": item[
                            "chunk_id"
                        ],
                        "text": item["text"],
                    },
                )
            )


        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )


        print(
            f"Added {len(points)} embeddings "
            f"to Qdrant."
        )


    def search(
        self,
        query_embedding,
        limit=5,
    ):

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=limit,
        ).points

        return results


vector_store = VectorStore()