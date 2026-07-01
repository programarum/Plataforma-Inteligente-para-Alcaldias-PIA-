"""Framework-independent role commands."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateRole:
    municipality_id: UUID
    name: str
    description: str
    is_system: bool = False
    is_active: bool = True


@dataclass(frozen=True, slots=True)
class UpdateRole:
    name: str | None = None
    description: str | None = None


@dataclass(frozen=True, slots=True)
class AssignPermission:
    permission_id: UUID

