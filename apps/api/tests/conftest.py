"""Shared pytest fixtures for API tests."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture
def configured_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set deterministic application settings for the test process."""
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


@pytest.fixture
def db_session(configured_environment: None) -> Generator[Session, None, None]:
    """Provide a transaction-capable in-memory database session."""
    from app.core.database import Base
    from app.modules.audit.infrastructure.models import AuditLogModel
    from app.modules.departments.infrastructure.models import DepartmentModel
    from app.modules.municipalities.infrastructure.models import MunicipalityModel

    registered_models = (AuditLogModel, DepartmentModel, MunicipalityModel)
    assert registered_models

    test_engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(test_engine)
    testing_session = sessionmaker(
        bind=test_engine,
        autoflush=False,
        expire_on_commit=False,
    )

    with testing_session() as session:
        yield session

    Base.metadata.drop_all(test_engine)
    test_engine.dispose()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Provide a test client with application lifespan management."""
    from app.core.database import get_db_session
    from app.main import app

    def override_db_session() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db_session] = override_db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
