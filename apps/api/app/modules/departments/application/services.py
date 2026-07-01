"""Department application use cases."""

from collections.abc import Mapping
from typing import cast
from uuid import UUID

from app.modules.departments.domain.entities import Department, utc_now
from app.modules.departments.domain.repositories import DepartmentRepository
from app.modules.municipalities.domain.repositories import MunicipalityRepository
from app.shared.exceptions import EntityNotFoundError


class DepartmentService:
    """Coordinate department use cases through repository contracts."""

    def __init__(
        self,
        repository: DepartmentRepository,
        municipality_repository: MunicipalityRepository,
    ) -> None:
        """Initialize the service with department and municipality boundaries."""
        self._repository = repository
        self._municipality_repository = municipality_repository

    def create(
        self,
        *,
        municipality_id: UUID,
        name: str,
        description: str | None,
        manager_name: str | None,
    ) -> Department:
        """Create an active department for an existing municipality."""
        if self._municipality_repository.get(municipality_id) is None:
            raise EntityNotFoundError("Municipality", municipality_id)

        department = Department(
            municipality_id=municipality_id,
            name=name,
            description=description,
            manager_name=manager_name,
        )
        return self._repository.add(department)

    def list(self) -> list[Department]:
        """List all departments."""
        return self._repository.list()

    def get(self, department_id: UUID) -> Department:
        """Get a department or report that it does not exist."""
        department = self._repository.get(department_id)
        if department is None:
            raise EntityNotFoundError("Department", department_id)
        return department

    def update(self, department_id: UUID, changes: Mapping[str, object]) -> Department:
        """Apply supported partial changes to a department."""
        department = self.get(department_id)

        if "name" in changes:
            department.name = cast(str, changes["name"])
        if "description" in changes:
            department.description = cast(str | None, changes["description"])
        if "manager_name" in changes:
            department.manager_name = cast(str | None, changes["manager_name"])

        department.updated_at = utc_now()
        return self._repository.update(department)

    def deactivate(self, department_id: UUID) -> Department:
        """Mark a department as inactive without deleting its history."""
        department = self.get(department_id)
        department.is_active = False
        department.updated_at = utc_now()
        return self._repository.update(department)
