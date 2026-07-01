"""Repository contracts for departments."""

from typing import Protocol
from uuid import UUID

from app.modules.departments.domain.entities import Department


class DepartmentRepository(Protocol):
    """Define persistence operations required by department use cases."""

    def add(self, department: Department) -> Department:
        """Persist and return a department."""
        ...

    def list(self) -> list[Department]:
        """Return all departments."""
        ...

    def get(self, department_id: UUID) -> Department | None:
        """Return a department by identifier when it exists."""
        ...

    def update(self, department: Department) -> Department:
        """Persist changes to an existing department."""
        ...
