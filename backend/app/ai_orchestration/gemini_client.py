import os
import google.generativeai as genai
from typing import Dict, Any

class GeminiClient:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing.")
        genai.configure(api_key=api_key)
        # Using the recommended model for text processing
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def analyze_contract(self, text: str) -> str:
        """
        Sends the contract text to Gemini to identify legal risks, clauses, and summaries.
        """
        prompt = f"""
        You are an expert legal AI assistant. Analyze the following contract text.
        Provide a structured analysis including:
        1. Summary: A brief executive summary of the document.
        2. Key Clauses: Identify 3-5 important clauses.
        3. Potential Risks: Identify any unusual, risky, or heavily one-sided terms.

        Contract Text:
        {text}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Handle potential API errors gracefully
            raise RuntimeError(f"Error during Gemini API call: {str(e)}")

    async def _run_agent_async(self, role_prompt: str, text: str) -> str:
        prompt = f"{role_prompt}\n\nContract Text:\n{text}"
        response = await self.model.generate_content_async(prompt)
        return response.text

    async def agent_financial_async(self, text: str) -> str:
        role = "You are the Financial Risk AI Agent. Analyze the contract strictly for financial liabilities, hidden fees, auto-renewals, and unfair payment terms. Output your findings in a concise markdown format, using bullet points."
        return await self._run_agent_async(role, text)

    async def agent_liability_async(self, text: str) -> str:
        role = "You are the Legal Liability AI Agent. Analyze the contract strictly for indemnification clauses, one-sided arbitration, termination penalties, and liability waivers. Output your findings in a concise markdown format, using bullet points."
        return await self._run_agent_async(role, text)

    async def agent_privacy_async(self, text: str) -> str:
        role = "You are the Privacy & Data Security AI Agent. Analyze the contract strictly for excessive data collection, intellectual property transfers, and privacy violations. Output your findings in a concise markdown format, using bullet points."
        return await self._run_agent_async(role, text)

    async def chat_with_contract_async(self, text: str, question: str) -> str:
        """Allows conversational Q&A against the contract text."""
        prompt = f"""
        You are a highly knowledgeable Legal Assistant AI.
        Below is the text of a contract. Based ONLY on the contract text provided, answer the user's question clearly, concisely, and accurately.
        If the contract does not contain information to answer the question, state that clearly.

        Contract Text:
        {text}

        User Question:
        {question}
        """
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error during Gemini Chat API call: {str(e)}")

# Singleton instance
gemini_client = None

def get_gemini_client() -> GeminiClient:
    global gemini_client
    if gemini_client is None:
        gemini_client = GeminiClient()
    return gemini_client
