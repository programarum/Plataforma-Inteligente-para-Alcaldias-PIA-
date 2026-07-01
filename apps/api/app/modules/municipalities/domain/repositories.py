"""Repository contracts for municipalities."""

from typing import Protocol
from uuid import UUID

from app.modules.municipalities.domain.entities import Municipality


class MunicipalityRepository(Protocol):
    """Define persistence operations required by municipality use cases."""

    def add(self, municipality: Municipality) -> Municipality:
        """Persist and return a municipality."""
        ...

    def list(self) -> list[Municipality]:
        """Return all municipalities."""
        ...

    def get(self, municipality_id: UUID) -> Municipality | None:
        """Return a municipality by identifier when it exists."""
        ...

    def update(self, municipality: Municipality) -> Municipality:
        """Persist changes to an existing municipality."""
        ...
