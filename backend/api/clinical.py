from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.rag_generator import rag_generator


router = APIRouter()


class ClinicalQuestion(BaseModel):
    question: str


@router.post("/ask")
def ask_clinical_question(
    data: ClinicalQuestion
):
    result = rag_generator.generate_answer(
        data.question
    )

    verification = result["verification"]

    return {
        "question": result["query"],

        "answer": result["answer"],

        "evidence": [
            {
                "chunk_id": item["chunk_id"],
                "relevance_score": item["reranker_score"],
                "text": item["text"],
            }
            for item in result["evidence"]
        ],

        "verification": {
            "verification_score": verification[
                "verification_score"
            ],

            "verified_claims": verification[
                "verified_claims"
            ],

            "unsupported_claims": verification[
                "unsupported_claims"
            ],

            "contradicted_claims": verification[
                "contradicted_claims"
            ],
        },

        "disclaimer": (
            "This system provides evidence-based clinical "
            "decision support and does not replace a "
            "qualified healthcare professional."
        ),
    }