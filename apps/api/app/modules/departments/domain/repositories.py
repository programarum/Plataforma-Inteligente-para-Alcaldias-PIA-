"""Department repository port."""

from typing import Protocol
from uuid import UUID

from app.modules.departments.domain.models import Department


class DepartmentRepository(Protocol):
    """Persistence operations required by department use cases."""

    def add(self, department: Department) -> Department: ...

    def list(self) -> list[Department]: ...

    def get(self, department_id: UUID) -> Department | None: ...

    def save(self, department: Department) -> Department: ...

