import pytest
from pydantic import ValidationError

from app.schemas.analysis import TicketAnalysis


def valid_refund_analysis() -> dict[str, object]:
    return {
        "category": "BILLING",
        "priority": "HIGH",
        "summary": "Customer reports a duplicate charge.",
        "proposed_action": "CREATE_REFUND_REQUEST",
        "requires_approval": True,
        "knowledge_query": "duplicate charge refund policy",
        "response_draft": "The case is ready for human review.",
    }


def test_protected_action_requires_approval() -> None:
    data = valid_refund_analysis()
    data["requires_approval"] = False

    with pytest.raises(ValidationError):
        TicketAnalysis.model_validate(data)


def test_extra_provider_fields_are_rejected() -> None:
    data = valid_refund_analysis()
    data["unexpected_field"] = "must not pass validation"

    with pytest.raises(ValidationError):
        TicketAnalysis.model_validate(data)


def test_valid_protected_action_passes() -> None:
    analysis = TicketAnalysis.model_validate(valid_refund_analysis())

    assert analysis.proposed_action.value == "CREATE_REFUND_REQUEST"
    assert analysis.requires_approval is True
