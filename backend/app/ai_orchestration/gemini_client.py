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

# Singleton instance
gemini_client = None

def get_gemini_client() -> GeminiClient:
    global gemini_client
    if gemini_client is None:
        gemini_client = GeminiClient()
    return gemini_client
