"""SQLAlchemy department repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.departments.domain.models import Department


class SQLAlchemyDepartmentRepository:
    """Persist departments in the current SQLAlchemy session."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, department: Department) -> Department:
        self._session.add(department)
        self._session.commit()
        self._session.refresh(department)
        return department

    def list(self) -> list[Department]:
        statement = select(Department).order_by(Department.created_at)
        return list(self._session.scalars(statement))

    def get(self, department_id: UUID) -> Department | None:
        return self._session.get(Department, department_id)

    def save(self, department: Department) -> Department:
        self._session.add(department)
        self._session.commit()
        self._session.refresh(department)
        return department

