from fastapi.testclient import TestClient

from app.main import app


def test_create_ticket_endpoint() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/tickets",
            json={
                "customer_email": "mark@example.com",
                "message": "I was charged twice and I need help.",
            },
        )

    assert response.status_code == 201
    body = response.json()
    assert body["customer_email"] == "mark@example.com"
    assert body["status"] == "NEW"
