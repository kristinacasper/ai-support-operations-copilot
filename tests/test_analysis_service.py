import pytest
from pydantic import ValidationError

from app.ai.mock_provider import MockAnalysisProvider
from app.services.analysis_service import analyze_ticket_preview


class InvalidProvider:
    def analyze(
        self,
        *,
        customer_email: str,
        message: str,
    ) -> dict[str, object]:
        return {
            "category": "NOT_A_REAL_CATEGORY",
            "priority": "HIGH",
            "summary": "Invalid provider output.",
            "proposed_action": "CREATE_REFUND_REQUEST",
            "requires_approval": False,
            "knowledge_query": "bad output",
            "response_draft": "This output must be rejected.",
        }


def test_mock_provider_returns_valid_billing_analysis() -> None:
    analysis = analyze_ticket_preview(
        MockAnalysisProvider(),
        customer_email="mark@example.com",
        message="I was charged twice and I need help.",
    )

    assert analysis.category.value == "BILLING"
    assert analysis.priority.value == "HIGH"
    assert analysis.requires_approval is True


def test_invalid_provider_output_is_rejected() -> None:
    with pytest.raises(ValidationError):
        analyze_ticket_preview(
            InvalidProvider(),
            customer_email="mark@example.com",
            message="I was charged twice and I need help.",
        )
