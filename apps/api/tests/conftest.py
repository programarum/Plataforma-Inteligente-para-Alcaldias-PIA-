"""Shared pytest fixtures."""

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

# Keep tests deterministic when the host defines generic variables such as DEBUG.
os.environ.update(
    {
        "APP_NAME": "PIA API",
        "APP_VERSION": "0.1.0",
        "ENVIRONMENT": "development",
        "DEBUG": "true",
        "DATABASE_URL": "postgresql+psycopg://pia:pia@postgres:5432/pia",
        "JWT_SECRET": "test-secret",
        "LOG_LEVEL": "INFO",
    }
)

from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Provide a FastAPI test client with lifespan handling."""
    with TestClient(app) as test_client:
        yield test_client
