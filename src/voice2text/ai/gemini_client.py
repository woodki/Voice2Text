from google import genai

class GeminiClient:
    def __init__(self, api_key):
        self.client = genai.Client(
            api_key=api_key
        )

    def generate(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )
        return response.text