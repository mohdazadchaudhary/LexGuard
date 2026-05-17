import io
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.services.analysis_service import AnalysisService

# ==========================================
# 1. Tests for __init__
# ==========================================

def test_should_initialize_analysis_service_successfully():
    """
    Happy-path: verify AnalysisService can be successfully constructed
    and correctly fetches the GeminiClient singleton.
    """
    # Arrange
    with patch("app.services.analysis_service.get_gemini_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Act
        service = AnalysisService()

        # Assert
        assert service.ai_client == mock_client
        mock_get_client.assert_called_once()


# ==========================================
# 2. Tests for extract_text_from_pdf
# ==========================================

@patch("app.services.analysis_service.pypdf.PdfReader")
def test_should_extract_text_from_pdf_when_valid_pdf_bytes_are_provided(mock_pdf_reader):
    """
    Happy-path: verify extract_text_from_pdf correctly extracts text
    from multiple pages of a mock PDF.
    """
    # Arrange
    service = AnalysisService()
    
    # Mocking pages list with text
    page1 = MagicMock()
    page1.extract_text.return_value = "Page 1 Content."
    page2 = MagicMock()
    page2.extract_text.return_value = "Page 2 Content."
    
    mock_reader = MagicMock()
    mock_reader.pages = [page1, page2]
    mock_pdf_reader.return_value = mock_reader
    
    pdf_bytes = b"%PDF-mock-bytes"

    # Act
    extracted_text = service.extract_text_from_pdf(pdf_bytes)

    # Assert
    assert extracted_text == "Page 1 Content.\nPage 2 Content."
    mock_pdf_reader.assert_called_once()
    # Verify we passed a BytesIO stream containing our bytes
    called_stream = mock_pdf_reader.call_args[0][0]
    assert isinstance(called_stream, io.BytesIO)
    assert called_stream.getvalue() == pdf_bytes


@patch("app.services.analysis_service.pypdf.PdfReader")
def test_should_raise_value_error_when_pdf_parsing_fails(mock_pdf_reader):
    """
    Failure-case: verify extract_text_from_pdf wraps pypdf parsing exceptions
    in a clean ValueError.
    """
    # Arrange
    service = AnalysisService()
    mock_pdf_reader.side_effect = Exception("Invalid file header")

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        service.extract_text_from_pdf(b"corrupted-bytes")

    assert "Failed to parse PDF: Invalid file header" in str(exc_info.value)


@patch("app.services.analysis_service.pypdf.PdfReader")
def test_should_handle_pdf_with_empty_pages_or_no_text(mock_pdf_reader):
    """
    Edge-case: verify extract_text_from_pdf doesn't crash and returns empty string
    when PDF pages yield None or blank strings.
    """
    # Arrange
    service = AnalysisService()
    
    page1 = MagicMock()
    page1.extract_text.return_value = None  # Scanned image, no OCR text
    page2 = MagicMock()
    page2.extract_text.return_value = "   "  # Blank page
    
    mock_reader = MagicMock()
    mock_reader.pages = [page1, page2]
    mock_pdf_reader.return_value = mock_reader

    # Act
    extracted_text = service.extract_text_from_pdf(b"mock")

    # Assert
    assert extracted_text == ""


# ==========================================
# 3. Tests for process_document_text
# ==========================================

@pytest.mark.asyncio
async def test_should_orchestrate_multi_agent_analysis_and_combine_reports():
    """
    Happy-path: verify process_document_text coordinates the financial, liability, and privacy
    agents concurrently and returns the combined markdown report.
    """
    # Arrange
    service = AnalysisService()
    mock_ai = MagicMock()
    service.ai_client = mock_ai
    
    mock_ai.agent_financial_async = AsyncMock(return_value="Financial details output")
    mock_ai.agent_liability_async = AsyncMock(return_value="Liability details output")
    mock_ai.agent_privacy_async = AsyncMock(return_value="Privacy details output")
    
    text = "We have a valid contract document contents here."

    # Act
    report = await service.process_document_text(text)

    # Assert
    assert "# LexGuard Multi-Agent Intelligence Report" in report
    assert "## 💰 Financial Risk Analysis" in report
    assert "Financial details output" in report
    assert "## ⚖️ Legal & Liability Analysis" in report
    assert "Liability details output" in report
    assert "## 🔒 Privacy & Data Security Analysis" in report
    assert "Privacy details output" in report

    mock_ai.agent_financial_async.assert_called_once_with(text)
    mock_ai.agent_liability_async.assert_called_once_with(text)
    mock_ai.agent_privacy_async.assert_called_once_with(text)


@pytest.mark.asyncio
async def test_should_raise_value_error_when_document_text_is_empty():
    """
    Failure-case: verify process_document_text rejects empty or whitespace-only document text.
    """
    # Arrange
    service = AnalysisService()

    # Act & Assert (Empty string)
    with pytest.raises(ValueError) as exc_info1:
        await service.process_document_text("")
    assert "Document text cannot be empty." in str(exc_info1.value)

    # Act & Assert (Whitespace)
    with pytest.raises(ValueError) as exc_info2:
        await service.process_document_text("   \n   ")
    assert "Document text cannot be empty." in str(exc_info2.value)


@pytest.mark.asyncio
async def test_should_handle_concurrent_agent_failures_safely():
    """
    Edge-case: verify that if one of the concurrent sub-agents throws an exception,
    the promise gather propagates the failure, and it is handled properly.
    """
    # Arrange
    service = AnalysisService()
    mock_ai = MagicMock()
    service.ai_client = mock_ai
    
    mock_ai.agent_financial_async = AsyncMock(return_value="Financial OK")
    mock_ai.agent_liability_async = AsyncMock(side_effect=Exception("Liability model timeout"))
    mock_ai.agent_privacy_async = AsyncMock(return_value="Privacy OK")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await service.process_document_text("valid contract")

    assert "Liability model timeout" in str(exc_info.value)


# ==========================================
# 4. Tests for chat_about_document
# ==========================================

@pytest.mark.asyncio
async def test_should_return_chat_answer_from_gemini_client():
    """
    Happy-path: verify chat_about_document delegates Q&A questions to Gemini
    and returns its final grounded answer.
    """
    # Arrange
    service = AnalysisService()
    mock_ai = MagicMock()
    service.ai_client = mock_ai
    mock_ai.chat_with_contract_async = AsyncMock(return_value="The answer is yes.")
    
    doc_text = "Standard mutual NDA contract text."
    question = "Is this contract mutual?"

    # Act
    answer = await service.chat_about_document(doc_text, question)

    # Assert
    assert answer == "The answer is yes."
    mock_ai.chat_with_contract_async.assert_called_once_with(doc_text, question)


@pytest.mark.asyncio
async def test_should_raise_value_error_when_inputs_are_empty():
    """
    Failure-case: verify chat_about_document rejects empty inputs.
    """
    # Arrange
    service = AnalysisService()
    
    # Case 1: Empty text
    with pytest.raises(ValueError) as exc_info1:
        await service.chat_about_document("", "Question?")
    assert "Document text cannot be empty." in str(exc_info1.value)

    # Case 2: Empty question
    with pytest.raises(ValueError) as exc_info2:
        await service.chat_about_document("Contract text", "")
    assert "Question cannot be empty." in str(exc_info2.value)


@pytest.mark.asyncio
async def test_should_propagate_underlying_api_errors_from_gemini_client():
    """
    Edge-case: verify that underlying runtime errors from the Gemini Client
    propagate upward cleanly without silencing or alteration.
    """
    # Arrange
    service = AnalysisService()
    mock_ai = MagicMock()
    service.ai_client = mock_ai
    mock_ai.chat_with_contract_async = AsyncMock(side_effect=RuntimeError("Gemini Chat Failure"))

    # Act & Assert
    with pytest.raises(RuntimeError) as exc_info:
        await service.chat_about_document("Valid contract text", "Who is the owner?")

    assert "Gemini Chat Failure" in str(exc_info.value)
