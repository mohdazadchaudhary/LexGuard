import fitz  # PyMuPDF
from app.ai_orchestration.gemini_client import get_gemini_client

class AnalysisService:
    def __init__(self):
        self.ai_client = get_gemini_client()

    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """Extracts text from a PDF file."""
        text = ""
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page in doc:
                text += page.get_text()
            return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")

    async def process_document_text(self, text: str) -> str:
        """
        Orchestrates the analysis of document text using a Multi-Agent architecture.
        Runs specific agents in parallel for specialized risk extraction.
        """
        import asyncio

        if not text or len(text.strip()) == 0:
            raise ValueError("Document text cannot be empty.")
            
        # Run specialized agents concurrently
        financial_task = self.ai_client.agent_financial_async(text)
        liability_task = self.ai_client.agent_liability_async(text)
        privacy_task = self.ai_client.agent_privacy_async(text)

        results = await asyncio.gather(financial_task, liability_task, privacy_task)
        
        # Combine the results into a single comprehensive report
        report = f"""# LexGuard Multi-Agent Intelligence Report

## 💰 Financial Risk Analysis
{results[0]}

---

## ⚖️ Legal & Liability Analysis
{results[1]}

---

## 🔒 Privacy & Data Security Analysis
{results[2]}
"""
        return report

    async def chat_about_document(self, text: str, question: str) -> str:
        """
        Answers a user question based on the provided document text.
        """
        if not text or len(text.strip()) == 0:
            raise ValueError("Document text cannot be empty.")
        if not question or len(question.strip()) == 0:
            raise ValueError("Question cannot be empty.")
            
        return await self.ai_client.chat_with_contract_async(text, question)
