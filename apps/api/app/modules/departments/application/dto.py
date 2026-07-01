"""Framework-independent department use-case input data."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateDepartment:
    municipality_id: UUID
    name: str
    description: str
    manager_name: str
    is_active: bool = True


@dataclass(frozen=True, slots=True)
class UpdateDepartment:
    name: str | None = None
    description: str | None = None
    manager_name: str | None = None

