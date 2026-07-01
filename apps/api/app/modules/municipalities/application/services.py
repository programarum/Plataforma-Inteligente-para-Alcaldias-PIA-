"""Municipality application use cases."""

from collections.abc import Mapping
from typing import cast
from uuid import UUID

from app.modules.municipalities.domain.entities import Municipality, utc_now
from app.modules.municipalities.domain.repositories import MunicipalityRepository
from app.shared.exceptions import EntityNotFoundError


class MunicipalityService:
    """Coordinate municipality use cases through a repository contract."""

    def __init__(self, repository: MunicipalityRepository) -> None:
        """Initialize the service with its persistence boundary."""
        self._repository = repository

    def create(
        self,
        *,
        name: str,
        department: str,
        country: str,
        mayor_name: str,
        government_period: str,
        mission: str | None,
        vision: str | None,
    ) -> Municipality:
        """Create an active municipality."""
        municipality = Municipality(
            name=name,
            department=department,
            country=country,
            mayor_name=mayor_name,
            government_period=government_period,
            mission=mission,
            vision=vision,
        )
        return self._repository.add(municipality)

    def list(self) -> list[Municipality]:
        """List all municipalities."""
        return self._repository.list()

    def get(self, municipality_id: UUID) -> Municipality:
        """Get a municipality or report that it does not exist."""
        municipality = self._repository.get(municipality_id)
        if municipality is None:
            raise EntityNotFoundError("Municipality", municipality_id)
        return municipality

    def update(
        self,
        municipality_id: UUID,
        changes: Mapping[str, object],
    ) -> Municipality:
        """Apply supported partial changes to a municipality."""
        municipality = self.get(municipality_id)

        if "name" in changes:
            municipality.name = cast(str, changes["name"])
        if "department" in changes:
            municipality.department = cast(str, changes["department"])
        if "country" in changes:
            municipality.country = cast(str, changes["country"])
        if "mayor_name" in changes:
            municipality.mayor_name = cast(str, changes["mayor_name"])
        if "government_period" in changes:
            municipality.government_period = cast(str, changes["government_period"])
        if "mission" in changes:
            municipality.mission = cast(str | None, changes["mission"])
        if "vision" in changes:
            municipality.vision = cast(str | None, changes["vision"])

        municipality.updated_at = utc_now()
        return self._repository.update(municipality)

    def deactivate(self, municipality_id: UUID) -> Municipality:
        """Mark a municipality as inactive without deleting its history."""
        municipality = self.get(municipality_id)
        municipality.is_active = False
        municipality.updated_at = utc_now()
        return self._repository.update(municipality)
