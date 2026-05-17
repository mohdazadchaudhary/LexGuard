import os
from google import genai
from google.genai import types
from PIL import Image
import io

# ---------------------------------------------------------------------------
# GeminiClient — wraps google-genai SDK for multi-agent legal analysis.
# Uses the singleton pattern so the API client is initialised once per process.
# ---------------------------------------------------------------------------

class GeminiClient:
    """
    Thin wrapper around the Google Gemini API (google-genai SDK).

    Provides specialized async agents for legal document analysis and a
    conversational Q&A interface.
    """

    def __init__(self) -> None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing.")
        self._client = genai.Client(api_key=api_key)
        # Primary model — 1.5-flash avoids free tier block issues of 2.0-flash.
        self._model_id = "gemini-1.5-flash"

    async def _generate_async(self, prompt: str) -> str:
        """
        Sends a text prompt to Gemini and returns the response text.

        @param prompt - The fully-formed prompt string.
        @returns Generated text from the model.
        @throws RuntimeError if the Gemini API call fails.
        """
        try:
            response = await self._client.aio.models.generate_content(
                model=self._model_id,
                contents=prompt,
            )
            return response.text
        except Exception as exc:
            raise RuntimeError(f"Gemini API error: {exc}") from exc

    async def extract_text_from_image_async(self, image_bytes: bytes) -> str:
        """
        Performs OCR on a document image using Gemini's multimodal capability.

        @param image_bytes - Raw bytes of the image file.
        @returns Extracted text from the image.
        @throws ValueError if OCR fails.
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            prompt = (
                "Perform high-fidelity OCR on this document image. Extract all text exactly "
                "as written, preserving structure and layout as much as possible. "
                "Output only the extracted text and nothing else."
            )
            response = await self._client.aio.models.generate_content(
                model=self._model_id,
                contents=[image, prompt],
            )
            return response.text.strip()
        except Exception as exc:
            raise ValueError(f"Failed to extract text from image: {exc}") from exc

    async def agent_financial_async(self, text: str) -> str:
        """
        Financial Risk AI Agent — identifies hidden fees, auto-renewals, payment terms.

        @param text - Contract text to analyse.
        @returns Markdown-formatted financial risk findings.
        """
        role = (
            "You are the Financial Risk AI Agent. Analyse the contract strictly for "
            "financial liabilities, hidden fees, auto-renewals, and unfair payment terms. "
            "Output your findings in concise markdown format, using bullet points."
        )
        return await self._generate_async(f"{role}\n\nContract Text:\n{text}")

    async def agent_liability_async(self, text: str) -> str:
        """
        Legal Liability AI Agent — reviews indemnification, arbitration, termination clauses.

        @param text - Contract text to analyse.
        @returns Markdown-formatted liability findings.
        """
        role = (
            "You are the Legal Liability AI Agent. Analyse the contract strictly for "
            "indemnification clauses, one-sided arbitration, termination penalties, and "
            "liability waivers. Output your findings in concise markdown format, using bullet points."
        )
        return await self._generate_async(f"{role}\n\nContract Text:\n{text}")

    async def agent_privacy_async(self, text: str) -> str:
        """
        Privacy & Data Security AI Agent — detects data collection and IP transfer issues.

        @param text - Contract text to analyse.
        @returns Markdown-formatted privacy/IP findings.
        """
        role = (
            "You are the Privacy & Data Security AI Agent. Analyse the contract strictly for "
            "excessive data collection, intellectual property transfers, and privacy violations. "
            "Output your findings in concise markdown format, using bullet points."
        )
        return await self._generate_async(f"{role}\n\nContract Text:\n{text}")

    async def chat_with_contract_async(self, text: str, question: str) -> str:
        """
        Answers a user question grounded in the provided contract text.

        @param text - Contract text serving as the knowledge base.
        @param question - User's natural-language question.
        @returns Accurate, contract-grounded answer.
        @throws RuntimeError if the Gemini API call fails.
        """
        prompt = (
            "You are a highly knowledgeable Legal Assistant AI.\n"
            "Below is the text of a contract. Based ONLY on the contract text provided, "
            "answer the user's question clearly, concisely, and accurately.\n"
            "If the contract does not contain information to answer the question, state that clearly.\n\n"
            f"Contract Text:\n{text}\n\n"
            f"User Question:\n{question}"
        )
        return await self._generate_async(prompt)


# ---------------------------------------------------------------------------
# Singleton accessor — avoids re-initialising the client on every request.
# ---------------------------------------------------------------------------
_gemini_client: GeminiClient | None = None


def get_gemini_client() -> GeminiClient:
    """
    Returns the module-level singleton GeminiClient, creating it on first call.

    @returns Shared GeminiClient instance.
    """
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client
