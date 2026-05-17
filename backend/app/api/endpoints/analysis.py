from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.analysis_service import AnalysisService

router = APIRouter()

class AnalysisRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    analysis: str

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
        result = service.process_document_text(request.text)
        return AnalysisResponse(analysis=result)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during analysis")
