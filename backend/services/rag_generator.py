from backend.services.evidence_retrieval import evidence_retriever
from backend.services.rag_context import rag_context_builder
from backend.services.llm_service import llm_service
from backend.services.evidence_verifier import evidence_verifier


class RAGGenerator:

    def generate_answer(self, query: str):

        # Step 1: Retrieve medical evidence
        evidence_results = evidence_retriever.search(
            query,
            retrieval_limit=10,
            final_limit=5
        )

        # Step 2: Build context for the LLM
        context = rag_context_builder.build_context(
            query,
            evidence_results
        )

        # Step 3: Generate an evidence-grounded answer
        prompt = f"""
You are an evidence-based clinical decision support assistant.

Your task is to answer the clinical question using ONLY information
directly supported by the retrieved medical evidence.

IMPORTANT RULES:

1. Do not invent medical facts.
2. Do not make a diagnosis.
3. Do not recommend treatment for an individual patient.
4. Do not treat article titles, references, or bibliography entries
   as medical evidence.
5. Only include claims that are directly supported by the retrieved
   evidence.
6. If evidence is insufficient, say:
   "The retrieved evidence is insufficient to answer this question."
7. Do not infer that a treatment is recommended merely because its
   name appears in the evidence.
8. Do not add information from your general medical knowledge.
9. Keep the answer concise.
10. This system provides clinical decision support and does not
    replace a qualified healthcare professional.

VERY IMPORTANT OUTPUT FORMAT:

Return ONLY separate numbered claims.

Use exactly this format:

1. <one complete claim>
2. <one complete claim>
3. <one complete claim>

Do NOT use bullet points inside a claim.
Do NOT use sub-points.
Do NOT add a conclusion.
Do NOT add a note.
Do NOT add information that is not directly supported by the evidence.

Clinical Question:
{query}

Retrieved Evidence:
{context}

Return only the numbered evidence-supported claims.
"""

        answer = llm_service.generate_response(
            prompt
        )

        # Step 4: Verify the generated claims
        verification = evidence_verifier.verify_claims(
            answer,
            evidence_results
        )

        # Step 5: Return answer + verification results
        return {
            "query": query,
            "answer": answer,
            "evidence": evidence_results,
            "verification": verification,
        }


rag_generator = RAGGenerator()