"""Framework-independent permission commands."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreatePermission:
    code: str
    name: str
    description: str
    module: str
    action: str
    is_active: bool = True


@dataclass(frozen=True, slots=True)
class UpdatePermission:
    code: str | None = None
    name: str | None = None
    description: str | None = None
    module: str | None = None
    action: str | None = None

