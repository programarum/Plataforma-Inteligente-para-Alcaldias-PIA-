"""Framework-independent municipality use-case input data."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateMunicipality:
    name: str
    department: str
    country: str
    mayor_name: str
    government_period: str
    mission: str
    vision: str
    is_active: bool = True


@dataclass(frozen=True, slots=True)
class UpdateMunicipality:
    name: str | None = None
    department: str | None = None
    country: str | None = None
    mayor_name: str | None = None
    government_period: str | None = None
    mission: str | None = None
    vision: str | None = None

