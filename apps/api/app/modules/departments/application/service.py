"""Department application use cases."""

from dataclasses import asdict
from uuid import UUID

from app.modules.departments.application.dto import CreateDepartment, UpdateDepartment
from app.modules.departments.domain.models import Department
from app.modules.departments.domain.repositories import DepartmentRepository
from app.modules.municipalities.domain.repositories import MunicipalityRepository
from app.shared.exceptions import NotFoundError


class DepartmentService:
    """Coordinate department lifecycle operations."""

    def __init__(
        self,
        repository: DepartmentRepository,
        municipality_repository: MunicipalityRepository,
    ) -> None:
        self._repository = repository
        self._municipality_repository = municipality_repository

    def create(self, command: CreateDepartment) -> Department:
        if self._municipality_repository.get(command.municipality_id) is None:
            raise NotFoundError("Municipality not found")
        return self._repository.add(Department(**asdict(command)))

    def list(self) -> list[Department]:
        return self._repository.list()

    def get(self, department_id: UUID) -> Department:
        department = self._repository.get(department_id)
        if department is None:
            raise NotFoundError("Department not found")
        return department

    def update(self, department_id: UUID, command: UpdateDepartment) -> Department:
        department = self.get(department_id)
        for field, value in asdict(command).items():
            if value is not None:
                setattr(department, field, value)
        return self._repository.save(department)

    def deactivate(self, department_id: UUID) -> Department:
        department = self.get(department_id)
        department.is_active = False
        return self._repository.save(department)

