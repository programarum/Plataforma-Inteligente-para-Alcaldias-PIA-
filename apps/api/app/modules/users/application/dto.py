"""Framework-independent user commands."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateUser:
    municipality_id: UUID
    department_id: UUID | None
    full_name: str
    email: str
    username: str
    password: str
    phone: str | None = None
    position: str | None = None
    is_active: bool = True
    is_superuser: bool = False


@dataclass(frozen=True, slots=True)
class UpdateUser:
    full_name: str | None = None
    email: str | None = None
    username: str | None = None
    phone: str | None = None
    position: str | None = None

