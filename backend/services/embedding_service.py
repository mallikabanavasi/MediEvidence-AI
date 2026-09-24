from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-m3"


class EmbeddingService:

    def __init__(self):
        print("Loading BGE-M3 embedding model...")
        self.model = SentenceTransformer(MODEL_NAME)
        print("BGE-M3 model loaded successfully.")

    def generate_embedding(self, text: str):
        """
        Convert one text into a 1024-dimensional embedding.
        """

        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()


embedding_service = EmbeddingService()