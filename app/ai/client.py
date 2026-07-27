import os

from dotenv import load_dotenv
from google import genai

from app.config import (
    DEFAULT_TEMPERATURE,
    GEMINI_MODEL,
)

load_dotenv()


class GeminiClient:
    """
    Wrapper around the Google Gemini API.
    """

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if api_key is None:
            raise ValueError(
                "GEMINI_API_KEY not found in .env"
            )

        self.client = genai.Client(api_key=api_key)

        self.model = GEMINI_MODEL

    def generate(
        self,
        prompt: str,
        temperature: float = DEFAULT_TEMPERATURE,
        response_mime_type: str = "text/plain",
    ) -> str:

        print("Sending request to Gemini...")

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "temperature": temperature,
                "response_mime_type": response_mime_type,
            },
        )

        print("Response received from Gemini.")

        return response.text


if __name__ == "__main__":

    print("Starting StudyOS AI client...")
    print(f"Using model: {GEMINI_MODEL}")

    client = GeminiClient()

    response = client.generate(
        "Reply with exactly one word: SUCCESS"
    )

    print("\nGemini Response:\n")
    print(response)
