"""Audit domain entities."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


def utc_now() -> datetime:
    """Return the current timezone-aware UTC timestamp."""
    return datetime.now(UTC)


@dataclass(slots=True)
class AuditLog:
    """Represent an immutable record of an institutional action."""

    actor_id: UUID
    action: str
    entity_type: str
    entity_id: UUID
    metadata: dict[str, object] = field(default_factory=dict)
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)
