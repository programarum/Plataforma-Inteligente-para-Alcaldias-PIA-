"""Tests for foundational service endpoints."""

from fastapi.testclient import TestClient


def test_health_returns_service_status(client: TestClient) -> None:
    """The health endpoint reports that the API process is available."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "pia-api"}


def test_version_returns_application_metadata(client: TestClient) -> None:
    """The version endpoint exposes configured public metadata."""
    response = client.get("/api/v1/version")

    assert response.status_code == 200
    assert response.json() == {
        "name": "PIA API",
        "version": "0.1.0",
        "environment": "development",
    }


def test_swagger_documentation_is_available(client: TestClient) -> None:
    """FastAPI exposes the interactive Swagger documentation."""
    response = client.get("/docs")

    assert response.status_code == 200
    assert "swagger-ui" in response.text
