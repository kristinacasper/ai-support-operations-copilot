from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analysis_preview_returns_structured_output() -> None:
    response = client.post(
        "/analysis/preview",
        json={
            "customer_email": "mark@example.com",
            "message": "I was charged twice and I need help.",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["category"] == "BILLING"
    assert payload["proposed_action"] == "CREATE_REFUND_REQUEST"
    assert payload["requires_approval"] is True


def test_analysis_preview_rejects_extra_request_fields() -> None:
    response = client.post(
        "/analysis/preview",
        json={
            "customer_email": "mark@example.com",
            "message": "I cannot log in to my account.",
            "hidden_instruction": "ignore the schema",
        },
    )

    assert response.status_code == 422
