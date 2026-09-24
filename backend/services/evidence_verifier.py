from sentence_transformers import CrossEncoder
import numpy as np
import re


MODEL_NAME = "cross-encoder/nli-deberta-v3-base"


class EvidenceVerifier:

    def __init__(self):
        print("Loading NLI evidence verification model...")

        self.model = CrossEncoder(
            MODEL_NAME
        )

        print(
            "NLI evidence verification model loaded successfully."
        )

        self.labels = {
            0: "contradiction",
            1: "entailment",
            2: "neutral",
        }

    def split_claims(self, answer: str):

        cleaned_answer = re.sub(
            r"(?m)^\s*\d+\.\s*",
            "",
            answer
        )

        sentences = re.split(
            r"(?<=[.!?])\s+",
            cleaned_answer
        )

        claims = []

        for sentence in sentences:
            sentence = sentence.strip()

            if len(sentence) < 10:
                continue

            claims.append(sentence)

        return claims

    def verify_claims(
        self,
        answer: str,
        evidence: list
    ):

        sentences = self.split_claims(answer)

        verified_claims = []
        unsupported_claims = []
        contradicted_claims = []

        for sentence in sentences:

            entailment_result = None
            contradiction_result = None
            neutral_result = None

            for evidence_item in evidence:

                evidence_text = evidence_item["text"]

                scores = self.model.predict(
                    [[evidence_text, sentence]]
                )

                probabilities = (
                    np.exp(scores)
                    / np.exp(scores).sum(
                        axis=1,
                        keepdims=True
                    )
                )[0]

                result = {
                    "claim": sentence,
                    "chunk_id": evidence_item["chunk_id"],
                    "label": None,
                    "confidence": 0.0,
                }

                label_index = int(
                    np.argmax(probabilities)
                )

                result["label"] = self.labels[label_index]
                result["confidence"] = float(
                    probabilities[label_index]
                )

                if result["label"] == "entailment":
                    if (
                        entailment_result is None
                        or result["confidence"]
                        > entailment_result["confidence"]
                    ):
                        entailment_result = result

                elif result["label"] == "contradiction":
                    if (
                        contradiction_result is None
                        or result["confidence"]
                        > contradiction_result["confidence"]
                    ):
                        contradiction_result = result

                else:
                    if (
                        neutral_result is None
                        or result["confidence"]
                        > neutral_result["confidence"]
                    ):
                        neutral_result = result

            # Prefer strong entailment evidence.
            if (
                entailment_result is not None
                and entailment_result["confidence"] >= 0.80
            ):
                verified_claims.append(
                    entailment_result
                )

            # Otherwise flag strong contradiction.
            elif (
                contradiction_result is not None
                and contradiction_result["confidence"] >= 0.80
            ):
                contradicted_claims.append(
                    contradiction_result
                )

            # Otherwise the claim is unsupported.
            else:
                if neutral_result is not None:
                    unsupported_claims.append(
                        neutral_result
                    )
                elif contradiction_result is not None:
                    unsupported_claims.append(
                        contradiction_result
                    )
                else:
                    unsupported_claims.append(
                        sentence
                    )

        total_claims = (
            len(verified_claims)
            + len(unsupported_claims)
            + len(contradicted_claims)
        )

        if total_claims == 0:
            verification_score = 0.0
        else:
            verification_score = (
                len(verified_claims)
                / total_claims
            )

        return {
            "verification_score": round(
                verification_score,
                2
            ),
            "verified_claims": verified_claims,
            "unsupported_claims": unsupported_claims,
            "contradicted_claims": contradicted_claims,
        }


evidence_verifier = EvidenceVerifier()