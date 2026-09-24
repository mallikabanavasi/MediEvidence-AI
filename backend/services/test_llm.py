from backend.services.llm_service import llm_service


prompt = """
You are a medical evidence assistant.

Answer the following question using only the information
provided below.

Question:
What are the treatment options for hypertension?

Evidence:
The retrieved evidence states that lifestyle interventions
and several classes of antihypertensive drugs can be used
for hypertension treatment. These include diuretics,
ACE-inhibitors, calcium antagonists, beta-blockers, and
angiotensin II receptor antagonists.

Do not make a diagnosis.
Do not add medical facts that are not present in the evidence.
"""


answer = llm_service.generate_response(
    prompt
)


print()
print("LLM Response")
print("=" * 60)
print()
print(answer)