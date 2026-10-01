from fastapi.testclient import TestClient

from app.main import app


def test_demo_customer_lookup_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/customers/lookup", params={"email": "mark@example.com"})

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "mark@example.com"
    assert body["is_demo"] is True


def test_missing_customer_returns_404() -> None:
    with TestClient(app) as client:
        response = client.get(
            "/customers/lookup",
            params={"email": "missing@example.com"},
        )

    assert response.status_code == 404


def test_knowledge_search_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/knowledge/search", params={"q": "duplicate charge"})

    assert response.status_code == 200
    results = response.json()
    assert results
    assert results[0]["topic"] == "billing"
