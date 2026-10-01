from types import SimpleNamespace

import pytest

from app.ai.factory import build_analysis_provider
from app.ai.mock_provider import MockAnalysisProvider
from app.ai.openai_provider import OpenAIAnalysisProvider


def test_factory_defaults_to_mock_provider() -> None:
    settings = SimpleNamespace(
        analysis_provider="mock",
        openai_api_key=None,
        openai_model="gpt-6-luna",
    )
    provider = build_analysis_provider(settings)
    assert isinstance(provider, MockAnalysisProvider)


def test_factory_builds_openai_provider_when_configured(monkeypatch) -> None:
    created = {}

    class FakeOpenAIProvider:
        def __init__(self, *, api_key, model):
            created["api_key"] = api_key
            created["model"] = model

    monkeypatch.setattr("app.ai.factory.OpenAIAnalysisProvider", FakeOpenAIProvider)

    settings = SimpleNamespace(
        analysis_provider="openai",
        openai_api_key="test-key",
        openai_model="gpt-6-luna",
    )
    provider = build_analysis_provider(settings)

    assert isinstance(provider, FakeOpenAIProvider)
    assert created == {"api_key": "test-key", "model": "gpt-6-luna"}


def test_factory_rejects_unknown_provider() -> None:
    settings = SimpleNamespace(
        analysis_provider="unknown",
        openai_api_key=None,
        openai_model="gpt-6-luna",
    )

    with pytest.raises(ValueError, match="Unsupported ANALYSIS_PROVIDER"):
        build_analysis_provider(settings)
