"""SQLAlchemy municipality repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.municipalities.domain.models import Municipality


class SQLAlchemyMunicipalityRepository:
    """Persist municipalities in the current SQLAlchemy session."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, municipality: Municipality) -> Municipality:
        self._session.add(municipality)
        self._session.commit()
        self._session.refresh(municipality)
        return municipality

    def list(self) -> list[Municipality]:
        statement = select(Municipality).order_by(Municipality.created_at)
        return list(self._session.scalars(statement))

    def get(self, municipality_id: UUID) -> Municipality | None:
        return self._session.get(Municipality, municipality_id)

    def save(self, municipality: Municipality) -> Municipality:
        self._session.add(municipality)
        self._session.commit()
        self._session.refresh(municipality)
        return municipality

