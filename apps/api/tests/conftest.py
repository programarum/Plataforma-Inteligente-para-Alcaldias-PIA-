"""Shared pytest fixtures."""

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

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

from app.core.database import Base, get_db
from app.main import app
from app.modules.audit.domain.models import AuditLog  # noqa: F401

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(
    bind=test_engine, class_=Session, expire_on_commit=False
)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Provide a FastAPI test client with lifespan handling."""
    Base.metadata.create_all(bind=test_engine)

    def override_get_db() -> Generator[Session, None, None]:
        with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
