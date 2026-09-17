class EnglishCorrector:
    def __init__(self, client):
        self.client = client
    def correct(self, text):
        prompt = f"""
        Please correct the following English text.

        Requirements:
        1. Correct grammar mistakes.
        2. Make unnatural expressions more natural.
        3. Keep the original meaning.
        4. Return the corrected version first.
        5. Then briefly explain the important corrections.

        Text:
        {text}
        """
        result = self.client.generate(prompt)
        return result