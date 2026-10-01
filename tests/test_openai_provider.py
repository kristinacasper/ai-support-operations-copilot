import json
from types import SimpleNamespace

import pytest

from app.ai.openai_provider import OpenAIAnalysisProvider


VALID_PAYLOAD = {
    "category": "BILLING",
    "priority": "HIGH",
    "summary": "Customer reports a duplicate subscription charge.",
    "proposed_action": "CREATE_REFUND_REQUEST",
    "requires_approval": True,
    "knowledge_query": "duplicate charge refund policy",
    "response_draft": "Thanks for reporting this. I can help review the duplicate charge before any refund request is submitted.",
}


class FakeResponses:
    def __init__(self, output_text: str) -> None:
        self.output_text = output_text
        self.last_kwargs = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        return SimpleNamespace(output_text=self.output_text)


class FakeClient:
    def __init__(self, output_text: str) -> None:
        self.responses = FakeResponses(output_text)


def test_openai_provider_requests_strict_json_schema() -> None:
    client = FakeClient(json.dumps(VALID_PAYLOAD))
    provider = OpenAIAnalysisProvider(
        api_key=None,
        model="test-model",
        client=client,
    )

    result = provider.analyze(
        customer_email="mark@example.com",
        message="I was charged twice. Please refund me now.",
    )

    assert result == VALID_PAYLOAD
    request = client.responses.last_kwargs
    assert request["model"] == "test-model"
    assert request["text"]["format"]["type"] == "json_schema"
    assert request["text"]["format"]["strict"] is True
    assert request["text"]["format"]["schema"]["additionalProperties"] is False
    assert "untrusted" in request["instructions"].lower()
    assert "charged twice" in request["input"][0]["content"][0]["text"]


def test_openai_provider_rejects_invalid_json() -> None:
    provider = OpenAIAnalysisProvider(
        api_key=None,
        model="test-model",
        client=FakeClient("not-json"),
    )

    with pytest.raises(RuntimeError, match="invalid JSON"):
        provider.analyze(
            customer_email="mark@example.com",
            message="I cannot access my account.",
        )


def test_openai_provider_requires_key_without_injected_client() -> None:
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        OpenAIAnalysisProvider(api_key=None, model="test-model")
