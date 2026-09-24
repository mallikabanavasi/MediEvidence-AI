from backend.services.evidence_verifier import evidence_verifier


answer = """
Hypertension treatment includes diuretics and ACE-inhibitors.
Fixed low-dose combination drug therapy can be used to start treatment.
Bananas are the best treatment for hypertension.
"""


evidence = [
    {
        "chunk_id": "PMC11263159_chunk_009",
        "text": """
        All 5 classes of antihypertensive drugs,
        including diuretics and ACE-inhibitors,
        can be used. Fixed low-dose combination
        drug therapy represents the first choice
        to start treatment.
        """
    }
]


result = evidence_verifier.verify_claims(
    answer,
    evidence
)


print()
print("NLI Evidence Verification Test")
print("=" * 60)

print()
print("Verification Score:")
print(result["verification_score"])


print()
print("Verified Claims:")
for claim in result["verified_claims"]:
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
for claim in result["unsupported_claims"]:
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
for claim in result["contradicted_claims"]:
    print(
        "-",
        claim["claim"],
        "|",
        claim["label"],
        "|",
        round(claim["confidence"], 3)
    )