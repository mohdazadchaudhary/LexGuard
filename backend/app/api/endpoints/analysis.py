from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from app.services.analysis_service import AnalysisService

router = APIRouter()

class AnalysisRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    text: str
    question: str

class AnalysisResponse(BaseModel):
    analysis: str
    extracted_text: str | None = None

class ChatResponse(BaseModel):
    answer: str

def get_analysis_service() -> AnalysisService:
    return AnalysisService()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_document(
    request: AnalysisRequest,
    service: AnalysisService = Depends(get_analysis_service)
):
    """
    Analyzes a legal document text using the Gemini AI models.
    """
    try:
        result = await service.process_document_text(request.text)
        return AnalysisResponse(analysis=result, extracted_text=request.text)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/upload", response_model=AnalysisResponse)
async def upload_and_analyze(
    file: UploadFile = File(...),
    service: AnalysisService = Depends(get_analysis_service)
):
    """
    Uploads a PDF, extracts text, and analyzes it.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        contents = await file.read()
        text = service.extract_text_from_pdf(contents)
        result = await service.process_document_text(text)
        return AnalysisResponse(analysis=result, extracted_text=text)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/chat", response_model=ChatResponse)
async def chat_document(
    request: ChatRequest,
    service: AnalysisService = Depends(get_analysis_service)
):
    """
    Asks a question about the provided contract text using Gemini.
    """
    try:
        result = await service.chat_about_document(request.text, request.question)
        return ChatResponse(answer=result)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
