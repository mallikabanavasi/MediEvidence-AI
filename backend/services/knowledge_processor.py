import json
from pathlib import Path


RAW_FILE = Path("data/knowledge_base/raw/PMC8862760.json")
PROCESSED_FOLDER = Path("data/knowledge_base/processed")
OUTPUT_FILE = PROCESSED_FOLDER / "PMC8862760.txt"


ARTICLE_TITLE = (
    "SMART COVID Navigator, a Clinical Decision Support Tool "
    "for COVID-19 Treatment"
)

SOURCE = "PubMed Central"
PMCID = "PMC8862760"
LICENSE = "CC BY 4.0"


def extract_text_from_bioc(data):
    """
    Extract article text from a PMC BioC JSON file.
    """

    text_parts = []

    for collection in data:

        for document in collection.get("documents", []):

            for passage in document.get("passages", []):

                text = passage.get("text", "").strip()

                if text:
                    text_parts.append(text)

    return "\n\n".join(text_parts)


def process_article():

    if not RAW_FILE.exists():
        print("Raw article file was not found.")
        return

    PROCESSED_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        RAW_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    article_text = extract_text_from_bioc(data)

    metadata = (
        f"Title: {ARTICLE_TITLE}\n"
        f"Source: {SOURCE}\n"
        f"PMCID: {PMCID}\n"
        f"License: {LICENSE}\n"
        f"\n"
        f"{'-' * 60}\n\n"
    )

    final_text = metadata + article_text

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(final_text)

    print("Article processed successfully!")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Characters extracted: {len(article_text)}")


if __name__ == "__main__":
    process_article()