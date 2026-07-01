"""Municipality domain entities."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


def utc_now() -> datetime:
    """Return the current timezone-aware UTC timestamp."""
    return datetime.now(UTC)


@dataclass(slots=True)
class Municipality:
    """Represent a municipal government supported by PIA."""

    name: str
    department: str
    country: str
    mayor_name: str
    government_period: str
    mission: str | None = None
    vision: str | None = None
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
