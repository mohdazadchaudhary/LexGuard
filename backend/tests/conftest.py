import os
import pytest
from unittest.mock import patch

# Set a mock GEMINI_API_KEY in the environment for all tests before any module imports
os.environ["GEMINI_API_KEY"] = "mock_api_key_value_for_testing"

@pytest.fixture(autouse=True)
def mock_settings_env():
    """Ensure mock environment variables are consistently present across all tests."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": "mock_api_key_value_for_testing"}):
        yield
