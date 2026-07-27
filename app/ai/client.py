import os

from dotenv import load_dotenv
from google import genai


class GeminiClient:
    """
    Reusable client for interacting with Google's Gemini API.
    """

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if api_key is None:
            raise ValueError(
                "GEMINI_API_KEY not found in .env"
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "models/gemini-flash-lite-latest"

    def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
    ) -> str:
        """
        Generate text using Gemini.
        """

        print("Sending request to Gemini...")

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "temperature": temperature,
            },
        )

        print("Response received from Gemini.")

        return response.text.strip()


if __name__ == "__main__":

    print("Starting StudyOS AI client...")

    client = GeminiClient()

    print(f"Using model: {client.model}")

    response = client.generate(
        "Reply with exactly the word: SUCCESS"
    )

    print("\nGemini Response:\n")

    print(response)
