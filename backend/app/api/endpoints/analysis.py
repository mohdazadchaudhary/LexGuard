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
    Uploads a document (PDF, DOCX, TXT, or Image), extracts text, and analyzes it.
    """
    filename = file.filename.lower()
    allowed_extensions = (".pdf", ".docx", ".txt", ".png", ".jpg", ".jpeg")
    if not filename.endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Only PDF, DOCX, TXT, and Image (PNG/JPG) are supported."
        )
    
    try:
        contents = await file.read()
        if filename.endswith(".pdf"):
            text = service.extract_text_from_pdf(contents)
        elif filename.endswith(".docx"):
            text = service.extract_text_from_docx(contents)
        elif filename.endswith((".png", ".jpg", ".jpeg")):
            text = await service.extract_text_from_image_async(contents)
        else: # .txt
            text = service.extract_text_from_txt(contents)
            
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
