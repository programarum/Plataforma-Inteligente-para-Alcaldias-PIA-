"""System endpoint tests."""

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "pia-api"}


def test_version(client: TestClient) -> None:
    response = client.get("/api/v1/version")

    assert response.status_code == 200
    assert response.json() == {
        "name": "PIA API",
        "version": "0.1.0",
        "environment": "development",
    }


def test_swagger_is_available(client: TestClient) -> None:
    response = client.get("/docs")

    assert response.status_code == 200
    assert "swagger-ui" in response.text

