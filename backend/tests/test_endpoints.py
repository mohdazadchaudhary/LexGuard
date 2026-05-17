import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from app.main import app
from app.api.endpoints.analysis import get_analysis_service, AnalysisResponse, ChatResponse

# Initialize standard FastAPI TestClient
client = TestClient(app)

# ==========================================
# 1. Tests for app.main Root & Health
# ==========================================

def test_should_return_success_on_root_endpoint():
    """
    Happy-path: verify GET / returns welcome message.
    """
    # Arrange & Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to LexGuard API. The system is running."}


def test_should_return_healthy_on_health_check_endpoint():
    """
    Happy-path: verify GET /health returns status healthy.
    """
    # Arrange & Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


# ==========================================
# 2. Tests for POST /analyze
# ==========================================

def test_should_analyze_document_text_and_return_report():
    """
    Happy-path: verify POST /api/v1/analysis/analyze processes input text
    and returns a valid AnalysisResponse containing the markdown analysis.
    """
    # Arrange
    mock_service = MagicMock()
    mock_service.process_document_text = AsyncMock(return_value="Detailed legal report analysis findings")
    app.dependency_overrides[get_analysis_service] = lambda: mock_service
    
    payload = {"text": "This is a mutual non-disclosure agreement."}

    try:
        # Act
        response = client.post("/api/v1/analysis/analyze", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["analysis"] == "Detailed legal report analysis findings"
        assert data["extracted_text"] == payload["text"]
        mock_service.process_document_text.assert_called_once_with(payload["text"])
    finally:
        app.dependency_overrides.clear()


def test_should_return_bad_request_on_empty_payload_body():
    """
    Failure-case: verify POST /api/v1/analysis/analyze returns HTTP 400
    when document text validation fails in the underlying service layer (ValueError).
    """
    # Arrange
    mock_service = MagicMock()
    mock_service.process_document_text = AsyncMock(side_effect=ValueError("Document text cannot be empty."))
    app.dependency_overrides[get_analysis_service] = lambda: mock_service
    
    payload = {"text": ""}

    try:
        # Act
        response = client.post("/api/v1/analysis/analyze", json=payload)

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Document text cannot be empty."
    finally:
        app.dependency_overrides.clear()


def test_should_return_server_error_if_service_raises_unexpected_exception():
    """
    Edge-case: verify POST /api/v1/analysis/analyze returns HTTP 500
    if the analysis service raises an unexpected database or server Exception.
    """
    # Arrange
    mock_service = MagicMock()
    mock_service.process_document_text = AsyncMock(side_effect=Exception("Database connection lost"))
    app.dependency_overrides[get_analysis_service] = lambda: mock_service
    
    payload = {"text": "Valid contract"}

    try:
        # Act
        response = client.post("/api/v1/analysis/analyze", json=payload)

        # Assert
        assert response.status_code == 500
        assert "Internal server error: Database connection lost" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()


# ==========================================
# 3. Tests for POST /upload
# ==========================================

def test_should_upload_pdf_parse_and_return_analysis_report():
    """
    Happy-path: verify POST /api/v1/analysis/upload accepts a valid PDF file,
    extracts its text content, processes it, and returns the analysis payload.
    """
    # Arrange
    mock_service = MagicMock()
    mock_service.extract_text_from_pdf = MagicMock(return_value="Extracted contract PDF text")
    mock_service.process_document_text = AsyncMock(return_value="PDF Contract analysis report")
    app.dependency_overrides[get_analysis_service] = lambda: mock_service
    
    mock_pdf_content = b"%PDF-mock-binary"
    files = {"file": ("test_contract.pdf", mock_pdf_content, "application/pdf")}

    try:
        # Act
        response = client.post("/api/v1/analysis/upload", files=files)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["analysis"] == "PDF Contract analysis report"
        assert data["extracted_text"] == "Extracted contract PDF text"
        mock_service.extract_text_from_pdf.assert_called_once_with(mock_pdf_content)
        mock_service.process_document_text.assert_called_once_with("Extracted contract PDF text")
    finally:
        app.dependency_overrides.clear()


def test_should_return_bad_request_for_non_pdf_file_upload():
    """
    Failure-case: verify POST /api/v1/analysis/upload returns HTTP 400
    if the uploaded file is not a PDF (e.g., test_contract.txt).
    """
    # Arrange
    mock_service = MagicMock()
    app.dependency_overrides[get_analysis_service] = lambda: mock_service
    
    files = {"file": ("test_contract.txt", b"plain text content", "text/plain")}

    try:
        # Act
        response = client.post("/api/v1/analysis/upload", files=files)

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Only PDF files are supported."
        mock_service.extract_text_from_pdf.assert_not_called()
    finally:
        app.dependency_overrides.clear()


def test_should_return_server_error_when_parsing_service_crashes():
    """
    Edge-case: verify POST /api/v1/analysis/upload returns HTTP 500
    if the parser service throws an unexpected low-level library exception.
    """
    # Arrange
    mock_service = MagicMock()
    mock_service.extract_text_from_pdf.side_effect = Exception("Out of memory during OCR parsing")
    app.dependency_overrides[get_analysis_service] = lambda: mock_service
    
    files = {"file": ("contract.pdf", b"%PDF-content", "application/pdf")}

    try:
        # Act
        response = client.post("/api/v1/analysis/upload", files=files)

        # Assert
        assert response.status_code == 500
        assert "Internal server error: Out of memory during OCR parsing" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()


# ==========================================
# 4. Tests for POST /chat
# ==========================================

def test_should_post_q_and_a_question_and_receive_grounded_answer():
    """
    Happy-path: verify POST /api/v1/analysis/chat coordinates the question against document text
    and returns a grounded ChatResponse answer.
    """
    # Arrange
    mock_service = MagicMock()
    mock_service.chat_about_document = AsyncMock(return_value="Yes, Section 4 requires 30 days termination notice.")
    app.dependency_overrides[get_analysis_service] = lambda: mock_service
    
    payload = {
        "text": "Section 4. Termination by giving 30 days notice.",
        "question": "What is the termination notice period?"
    }

    try:
        # Act
        response = client.post("/api/v1/analysis/chat", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Yes, Section 4 requires 30 days termination notice."
        mock_service.chat_about_document.assert_called_once_with(payload["text"], payload["question"])
    finally:
        app.dependency_overrides.clear()


def test_should_return_bad_request_when_asking_empty_question():
    """
    Failure-case: verify POST /api/v1/analysis/chat returns HTTP 400
    when question parameters are empty (ValueError in service layer).
    """
    # Arrange
    mock_service = MagicMock()
    mock_service.chat_about_document = AsyncMock(side_effect=ValueError("Question cannot be empty."))
    app.dependency_overrides[get_analysis_service] = lambda: mock_service
    
    payload = {
        "text": "Valid contract text content",
        "question": ""
    }

    try:
        # Act
        response = client.post("/api/v1/analysis/chat", json=payload)

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Question cannot be empty."
    finally:
        app.dependency_overrides.clear()


def test_should_return_server_error_on_underlying_qa_runtime_exception():
    """
    Edge-case: verify POST /api/v1/analysis/chat returns HTTP 500
    if the AI Q&A router raises a general connection failure.
    """
    # Arrange
    mock_service = MagicMock()
    mock_service.chat_about_document = AsyncMock(side_effect=Exception("Service temporary unavailable"))
    app.dependency_overrides[get_analysis_service] = lambda: mock_service
    
    payload = {
        "text": "Contract context",
        "question": "Can I sue?"
    }

    try:
        # Act
        response = client.post("/api/v1/analysis/chat", json=payload)

        # Assert
        assert response.status_code == 500
        assert "Internal server error: Service temporary unavailable" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()
