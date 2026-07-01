"""Municipality repository port."""

from typing import Protocol
from uuid import UUID

from app.modules.municipalities.domain.models import Municipality


class MunicipalityRepository(Protocol):
    """Persistence operations required by municipality use cases."""

    def add(self, municipality: Municipality) -> Municipality: ...

    def list(self) -> list[Municipality]: ...

    def get(self, municipality_id: UUID) -> Municipality | None: ...

    def save(self, municipality: Municipality) -> Municipality: ...

