from backend.services.rag_generator import rag_generator


query = "What are the treatment options for hypertension?"


result = rag_generator.generate_answer(query)


print()
print("FINAL RAG ANSWER")
print("=" * 60)

print()
print("Question:")
print(result["query"])

print()
print("Answer:")
print(result["answer"])

print()
print("Evidence:")
print("-" * 60)

for index, evidence in enumerate(
    result["evidence"],
    start=1
):
    print()
    print(f"Evidence {index}")
    print(f"Chunk ID: {evidence['chunk_id']}")
    print(
        f"Reranker Score: "
        f"{evidence['reranker_score']:.4f}"
    )

print()
print("NLI EVIDENCE VERIFICATION")
print("=" * 60)

verification = result["verification"]

print()
print("Verification Score:")
print(verification["verification_score"])

print()
print("Verified Claims:")

for claim in verification["verified_claims"]:
    print(
        "-",
        claim["claim"],
        "|",
        claim["label"],
        "|",
        round(claim["confidence"], 3)
    )

print()
print("Unsupported Claims:")

for claim in verification["unsupported_claims"]:
    if isinstance(claim, dict):
        print(
            "-",
            claim["claim"],
            "|",
            claim["label"],
            "|",
            round(claim["confidence"], 3)
        )
    else:
        print("-", claim)

print()
print("Contradicted Claims:")

for claim in verification["contradicted_claims"]:
    print(
        "-",
        claim["claim"],
        "|",
        claim["label"],
        "|",
        round(claim["confidence"], 3)
    )