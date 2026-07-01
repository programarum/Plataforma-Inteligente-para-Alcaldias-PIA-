"""SQLAlchemy engine and session configuration."""

from collections.abc import Generator

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

metadata = MetaData()
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """Provide a transactional database session to request dependencies."""
    with SessionLocal() as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise

