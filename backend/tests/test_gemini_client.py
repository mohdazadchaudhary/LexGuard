import os
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.ai_orchestration.gemini_client import GeminiClient, get_gemini_client

# Mock response class to simulate Gemini's API response structure
class MockGeminiResponse:
    def __init__(self, text_content: str):
        self._text = text_content

    @property
    def text(self) -> str:
        return self._text


@pytest.fixture
def mock_genai():
    """Fixture to mock the google.generativeai library."""
    with patch("app.ai_orchestration.gemini_client.genai") as mock_lib:
        yield mock_lib


@pytest.fixture
def default_env():
    """Fixture to ensure GEMINI_API_KEY is present for standard client initialization."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": "mock_api_key_value"}):
        yield


# ==========================================
# 1. Tests for __init__ & get_gemini_client
# ==========================================

def test_should_initialize_client_when_api_key_is_provided(mock_genai, default_env):
    """
    Happy-path: verify GeminiClient configures the generative AI library
    and instantiates the correct model name when GEMINI_API_KEY is in environment.
    """
    # Arrange & Act
    client = GeminiClient()

    # Assert
    mock_genai.configure.assert_called_once_with(api_key="mock_api_key_value")
    mock_genai.GenerativeModel.assert_called_once_with("gemini-2.5-flash")
    assert client.model is not None


def test_should_raise_value_error_when_api_key_is_missing(mock_genai):
    """
    Failure-case: verify GeminiClient constructor raises ValueError
    when the GEMINI_API_KEY environment variable is missing.
    """
    # Arrange
    with patch.dict(os.environ, {}, clear=True):
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            GeminiClient()
        
        assert "GEMINI_API_KEY environment variable is missing." in str(exc_info.value)


def test_should_initialize_with_custom_api_key_from_env(mock_genai):
    """
    Edge-case: verify client handles non-standard, very long or special character keys in the env successfully.
    """
    # Arrange
    custom_key = "AIzaSySpecial-Key_With_Dashes_12345!"
    with patch.dict(os.environ, {"GEMINI_API_KEY": custom_key}):
        # Act
        client = GeminiClient()

        # Assert
        mock_genai.configure.assert_called_once_with(api_key=custom_key)
        assert client.model is not None


# ==========================================
# 2. Tests for analyze_contract (Sync)
# ==========================================

def test_should_return_analysis_report_when_text_is_provided(mock_genai, default_env):
    """
    Happy-path: verify analyze_contract returns expected summary and analysis string
    when given valid contract text.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content.return_value = MockGeminiResponse("Mock Contract Analysis Report")
    contract_text = "This is a contract text about mutual non-disclosure obligations."

    # Act
    result = client.analyze_contract(contract_text)

    # Assert
    assert result == "Mock Contract Analysis Report"
    mock_model.generate_content.assert_called_once()
    called_prompt = mock_model.generate_content.call_args[0][0]
    assert contract_text in called_prompt


def test_should_raise_runtime_error_when_api_call_fails(mock_genai, default_env):
    """
    Failure-case: verify analyze_contract raises RuntimeError with original message
    if the genai API call raises an exception.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content.side_effect = Exception("API connection timed out")

    # Act & Assert
    with pytest.raises(RuntimeError) as exc_info:
        client.analyze_contract("Sample contract")

    assert "Error during Gemini API call: API connection timed out" in str(exc_info.value)


def test_should_handle_empty_string_payload_without_crashing(mock_genai, default_env):
    """
    Edge-case: verify analyze_contract generates content even for empty or single-character string
    without raising pre-validation errors.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content.return_value = MockGeminiResponse("No contract content provided.")

    # Act
    result = client.analyze_contract("")

    # Assert
    assert result == "No contract content provided."
    mock_model.generate_content.assert_called_once()


# =======================================================
# 3. Tests for agent_financial_async (Async)
# =======================================================

@pytest.mark.asyncio
async def test_should_return_financial_report_when_valid_text_is_provided(mock_genai, default_env):
    """
    Happy-path: verify agent_financial_async sends specific financial system role prompt
    and returns async markdown findings successfully.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content_async = AsyncMock(return_value=MockGeminiResponse("Financial Findings: Auto-renewal detected"))
    contract = "The agreement shall automatically renew for successive 1-year terms unless cancelled."

    # Act
    result = await client.agent_financial_async(contract)

    # Assert
    assert result == "Financial Findings: Auto-renewal detected"
    mock_model.generate_content_async.assert_called_once()
    called_prompt = mock_model.generate_content_async.call_args[0][0]
    assert "Financial Risk AI Agent" in called_prompt
    assert contract in called_prompt


@pytest.mark.asyncio
async def test_should_raise_runtime_error_when_financial_agent_fails(mock_genai, default_env):
    """
    Failure-case: verify agent_financial_async raises RuntimeError on model processing failures.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content_async = AsyncMock(side_effect=Exception("Blocked safety filter"))

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await client.agent_financial_async("Contract text")

    assert "Blocked safety filter" in str(exc_info.value)


@pytest.mark.asyncio
async def test_should_process_short_or_empty_text_for_financial_agent(mock_genai, default_env):
    """
    Edge-case: verify agent_financial_async calls generate_content_async successfully even with whitespaces.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content_async = AsyncMock(return_value=MockGeminiResponse("Empty inputs analysed."))

    # Act
    result = await client.agent_financial_async("   ")

    # Assert
    assert result == "Empty inputs analysed."
    mock_model.generate_content_async.assert_called_once()


# =======================================================
# 4. Tests for agent_liability_async (Async)
# =======================================================

@pytest.mark.asyncio
async def test_should_return_liability_report_when_valid_text_is_provided(mock_genai, default_env):
    """
    Happy-path: verify agent_liability_async sends legal liability system role prompt.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content_async = AsyncMock(return_value=MockGeminiResponse("Liability Findings: Indemnification waiver found"))
    contract = "The provider will not indemnify the client for any consequential damages."

    # Act
    result = await client.agent_liability_async(contract)

    # Assert
    assert result == "Liability Findings: Indemnification waiver found"
    called_prompt = mock_model.generate_content_async.call_args[0][0]
    assert "Legal Liability AI Agent" in called_prompt


@pytest.mark.asyncio
async def test_should_raise_runtime_error_when_liability_agent_fails(mock_genai, default_env):
    """
    Failure-case: verify agent_liability_async raises error on generation failure.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content_async = AsyncMock(side_effect=Exception("Invalid model arguments"))

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await client.agent_liability_async("Contract text")
    assert "Invalid model arguments" in str(exc_info.value)


@pytest.mark.asyncio
async def test_should_process_short_or_empty_text_for_liability_agent(mock_genai, default_env):
    """
    Edge-case: verify agent_liability_async runs with blank strings.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content_async = AsyncMock(return_value=MockGeminiResponse("Blank liability data"))

    # Act
    result = await client.agent_liability_async("")

    # Assert
    assert result == "Blank liability data"


# =======================================================
# 5. Tests for agent_privacy_async (Async)
# =======================================================

@pytest.mark.asyncio
async def test_should_return_privacy_report_when_valid_text_is_provided(mock_genai, default_env):
    """
    Happy-path: verify agent_privacy_async sends privacy/data system role prompt.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content_async = AsyncMock(return_value=MockGeminiResponse("Privacy Findings: Data sharing with 3rd party"))

    # Act
    result = await client.agent_privacy_async("We share your browser cookies with ad networks.")

    # Assert
    assert result == "Privacy Findings: Data sharing with 3rd party"
    called_prompt = mock_model.generate_content_async.call_args[0][0]
    assert "Privacy & Data Security AI Agent" in called_prompt


@pytest.mark.asyncio
async def test_should_raise_runtime_error_when_privacy_agent_fails(mock_genai, default_env):
    """
    Failure-case: verify agent_privacy_async raises exception on API failure.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content_async = AsyncMock(side_effect=Exception("Quota exceeded"))

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await client.agent_privacy_async("Contract text")
    assert "Quota exceeded" in str(exc_info.value)


@pytest.mark.asyncio
async def test_should_process_short_or_empty_text_for_privacy_agent(mock_genai, default_env):
    """
    Edge-case: verify agent_privacy_async handles empty payload cleanly.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content_async = AsyncMock(return_value=MockGeminiResponse("Empty privacy check"))

    # Act
    result = await client.agent_privacy_async("")

    # Assert
    assert result == "Empty privacy check"


# =======================================================
# 6. Tests for chat_with_contract_async (Async)
# =======================================================

@pytest.mark.asyncio
async def test_should_return_grounded_answer_when_question_and_text_are_provided(mock_genai, default_env):
    """
    Happy-path: verify chat_with_contract_async formats the contextual Q&A prompt
    and successfully returns the grounded response answer.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content_async = AsyncMock(return_value=MockGeminiResponse("The governing law is the State of California."))
    contract = "This contract shall be governed by and construed in accordance with the laws of California."
    question = "What is the governing law of this contract?"

    # Act
    result = await client.chat_with_contract_async(contract, question)

    # Assert
    assert result == "The governing law is the State of California."
    mock_model.generate_content_async.assert_called_once()
    called_prompt = mock_model.generate_content_async.call_args[0][0]
    assert "highly knowledgeable Legal Assistant AI" in called_prompt
    assert contract in called_prompt
    assert question in called_prompt


@pytest.mark.asyncio
async def test_should_raise_runtime_error_when_chat_api_call_fails(mock_genai, default_env):
    """
    Failure-case: verify chat_with_contract_async wraps failures into a clean RuntimeError.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content_async = AsyncMock(side_effect=Exception("Internal model server error"))

    # Act & Assert
    with pytest.raises(RuntimeError) as exc_info:
        await client.chat_with_contract_async("Contract", "Question")

    assert "Error during Gemini Chat API call: Internal model server error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_should_handle_empty_question_or_contract_gracefully(mock_genai, default_env):
    """
    Edge-case: verify chat_with_contract_async completes successfully when question or contract is empty strings.
    """
    # Arrange
    client = GeminiClient()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_model.generate_content_async = AsyncMock(return_value=MockGeminiResponse("No information found."))

    # Act
    result = await client.chat_with_contract_async("", "")

    # Assert
    assert result == "No information found."
