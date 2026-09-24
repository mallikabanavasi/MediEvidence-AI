from pathlib import Path
import re


INPUT_FOLDER = Path("data/knowledge_base/processed")
OUTPUT_FOLDER = Path(
    "data/knowledge_base/processed/chunks"
)

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def remove_references_section(text: str) -> str:
    """
    Remove the bibliography/reference section from
    an article before creating evidence chunks.
    """

    patterns = [
        r"\nReferences\s*\n",
        r"\nREFERENCES\s*\n",
        r"\nReferences\s*:",
        r"\nREFERENCES\s*:",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return text[:match.start()].strip()

    return text


def create_chunks(text: str):

    text = remove_references_section(text)

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - CHUNK_OVERLAP

    return chunks


def process_articles():

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    article_files = sorted(
        INPUT_FOLDER.glob("PMC*.txt")
    )

    total_chunks = 0

    for article_file in article_files:

        print()
        print(
            f"Processing: {article_file.name}"
        )

        text = article_file.read_text(
            encoding="utf-8"
        )

        chunks = create_chunks(text)

        pmcid = article_file.stem

        for index, chunk in enumerate(
            chunks,
            start=1
        ):

            output_file = (
                OUTPUT_FOLDER
                / f"{pmcid}_chunk_{index:03d}.txt"
            )

            output_file.write_text(
                chunk,
                encoding="utf-8"
            )

        print(
            f"Chunks created: {len(chunks)}"
        )

        total_chunks += len(chunks)

    print()
    print(
        "All articles chunked successfully!"
    )

    print(
        f"Total chunks: {total_chunks}"
    )

    print(
        f"Chunk folder: {OUTPUT_FOLDER}"
    )


if __name__ == "__main__":
    process_articles()