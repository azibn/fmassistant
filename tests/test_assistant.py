import pytest
from fmassistant.assistant import MODELS

def test_models_dict():
    """Test that the MODELS dictionary contains expected keys."""
    assert "claude" in MODELS
    assert "openai" in MODELS
    assert "ollama" in MODELS
    assert callable(MODELS["claude"])

