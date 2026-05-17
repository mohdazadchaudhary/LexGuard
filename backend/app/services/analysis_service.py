from app.ai_orchestration.gemini_client import get_gemini_client

class AnalysisService:
    def __init__(self):
        self.ai_client = get_gemini_client()

    def process_document_text(self, text: str) -> str:
        """
        Orchestrates the analysis of document text.
        In a full implementation, this might also involve saving to a database
        or performing OCR before analysis.
        """
        if not text or len(text.strip()) == 0:
            raise ValueError("Document text cannot be empty.")
            
        analysis_result = self.ai_client.analyze_contract(text)
        return analysis_result
