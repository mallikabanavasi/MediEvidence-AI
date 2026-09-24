import ollama


MODEL_NAME = "llama3.2:3b"


class LLMService:

    def generate_response(
        self,
        prompt: str
    ):

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]


llm_service = LLMService()