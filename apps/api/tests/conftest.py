"""Shared pytest fixtures for API tests."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    """Provide a test client with application lifespan management."""
    monkeypatch.setenv("APP_NAME", "PIA API")
    monkeypatch.setenv("APP_VERSION", "0.1.0")
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://pia:pia@postgres:5432/pia",
    )
    monkeypatch.setenv("JWT_SECRET", "change-me")
    monkeypatch.setenv("LOG_LEVEL", "INFO")

    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
