"""SQLAlchemy repository implementation for municipalities."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.municipalities.domain.entities import Municipality
from app.modules.municipalities.infrastructure.models import MunicipalityModel


class SqlAlchemyMunicipalityRepository:
    """Persist municipalities using a SQLAlchemy session."""

    def __init__(self, session: Session) -> None:
        """Initialize the repository with a unit-of-work session."""
        self._session = session

    def add(self, municipality: Municipality) -> Municipality:
        """Persist and return a municipality."""
        model = MunicipalityModel(
            id=municipality.id,
            name=municipality.name,
            department=municipality.department,
            country=municipality.country,
            mayor_name=municipality.mayor_name,
            government_period=municipality.government_period,
            mission=municipality.mission,
            vision=municipality.vision,
            is_active=municipality.is_active,
            created_at=municipality.created_at,
            updated_at=municipality.updated_at,
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def list(self) -> list[Municipality]:
        """Return all municipalities ordered by creation time."""
        statement = select(MunicipalityModel).order_by(MunicipalityModel.created_at)
        models = self._session.scalars(statement).all()
        return [self._to_entity(model) for model in models]

    def get(self, municipality_id: UUID) -> Municipality | None:
        """Return a municipality by identifier when it exists."""
        model = self._session.get(MunicipalityModel, municipality_id)
        return self._to_entity(model) if model is not None else None

    def update(self, municipality: Municipality) -> Municipality:
        """Persist changes to an existing municipality."""
        model = self._session.get(MunicipalityModel, municipality.id)
        if model is None:
            raise LookupError(f"Municipality '{municipality.id}' was not found")

        model.name = municipality.name
        model.department = municipality.department
        model.country = municipality.country
        model.mayor_name = municipality.mayor_name
        model.government_period = municipality.government_period
        model.mission = municipality.mission
        model.vision = municipality.vision
        model.is_active = municipality.is_active
        model.updated_at = municipality.updated_at
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: MunicipalityModel) -> Municipality:
        """Map a persistence model to a domain entity."""
        return Municipality(
            id=model.id,
            name=model.name,
            department=model.department,
            country=model.country,
            mayor_name=model.mayor_name,
            government_period=model.government_period,
            mission=model.mission,
            vision=model.vision,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
