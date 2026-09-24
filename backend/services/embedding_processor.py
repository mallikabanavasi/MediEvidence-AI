from pathlib import Path
import json

from backend.services.embedding_service import embedding_service


CHUNKS_FOLDER = Path(
    "data/knowledge_base/processed/chunks"
)

OUTPUT_FOLDER = Path(
    "data/knowledge_base/processed/embeddings"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER /
    "embeddings.json"
)


def generate_embeddings():

    if not CHUNKS_FOLDER.exists():

        print(
            "Chunks folder was not found."
        )

        return

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    chunk_files = sorted(
        CHUNKS_FOLDER.glob("PMC*_chunk_*.txt")
    )

    if not chunk_files:

        print(
            "No chunk files were found."
        )

        return

    embeddings_data = []

    print(
        f"Found {len(chunk_files)} chunks."
    )

    print(
        "Generating embeddings..."
    )

    for index, chunk_file in enumerate(
        chunk_files,
        start=1
    ):

        text = chunk_file.read_text(
            encoding="utf-8"
        ).strip()

        embedding = (
            embedding_service.generate_embedding(
                text
            )
        )

        embeddings_data.append(
            {
                "chunk_id": chunk_file.stem,
                "text": text,
                "embedding": embedding,
            }
        )

        print(
            f"Processed "
            f"{index}/{len(chunk_files)}: "
            f"{chunk_file.name}"
        )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            embeddings_data,
            file
        )

    print()

    print(
        "Embedding generation completed successfully!"
    )

    print(
        f"Total embeddings: "
        f"{len(embeddings_data)}"
    )

    print(
        f"Output file: {OUTPUT_FILE}"
    )


if __name__ == "__main__":

    generate_embeddings()