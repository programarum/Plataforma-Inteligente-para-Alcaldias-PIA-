"""SQLAlchemy repository implementation for departments."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.departments.domain.entities import Department
from app.modules.departments.infrastructure.models import DepartmentModel


class SqlAlchemyDepartmentRepository:
    """Persist departments using a SQLAlchemy session."""

    def __init__(self, session: Session) -> None:
        """Initialize the repository with a unit-of-work session."""
        self._session = session

    def add(self, department: Department) -> Department:
        """Persist and return a department."""
        model = DepartmentModel(
            id=department.id,
            municipality_id=department.municipality_id,
            name=department.name,
            description=department.description,
            manager_name=department.manager_name,
            is_active=department.is_active,
            created_at=department.created_at,
            updated_at=department.updated_at,
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def list(self) -> list[Department]:
        """Return all departments ordered by creation time."""
        statement = select(DepartmentModel).order_by(DepartmentModel.created_at)
        models = self._session.scalars(statement).all()
        return [self._to_entity(model) for model in models]

    def get(self, department_id: UUID) -> Department | None:
        """Return a department by identifier when it exists."""
        model = self._session.get(DepartmentModel, department_id)
        return self._to_entity(model) if model is not None else None

    def update(self, department: Department) -> Department:
        """Persist changes to an existing department."""
        model = self._session.get(DepartmentModel, department.id)
        if model is None:
            raise LookupError(f"Department '{department.id}' was not found")

        model.name = department.name
        model.description = department.description
        model.manager_name = department.manager_name
        model.is_active = department.is_active
        model.updated_at = department.updated_at
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: DepartmentModel) -> Department:
        """Map a persistence model to a domain entity."""
        return Department(
            id=model.id,
            municipality_id=model.municipality_id,
            name=model.name,
            description=model.description,
            manager_name=model.manager_name,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
