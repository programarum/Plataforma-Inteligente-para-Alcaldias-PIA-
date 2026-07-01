"""Municipality application use cases."""

from dataclasses import asdict
from uuid import UUID

from app.modules.municipalities.application.dto import (
    CreateMunicipality,
    UpdateMunicipality,
)
from app.modules.municipalities.domain.models import Municipality
from app.modules.municipalities.domain.repositories import MunicipalityRepository
from app.shared.exceptions import NotFoundError


class MunicipalityService:
    """Coordinate municipality lifecycle operations."""

    def __init__(self, repository: MunicipalityRepository) -> None:
        self._repository = repository

    def create(self, command: CreateMunicipality) -> Municipality:
        return self._repository.add(Municipality(**asdict(command)))

    def list(self) -> list[Municipality]:
        return self._repository.list()

    def get(self, municipality_id: UUID) -> Municipality:
        municipality = self._repository.get(municipality_id)
        if municipality is None:
            raise NotFoundError("Municipality not found")
        return municipality

    def update(
        self, municipality_id: UUID, command: UpdateMunicipality
    ) -> Municipality:
        municipality = self.get(municipality_id)
        for field, value in asdict(command).items():
            if value is not None:
                setattr(municipality, field, value)
        return self._repository.save(municipality)

    def deactivate(self, municipality_id: UUID) -> Municipality:
        municipality = self.get(municipality_id)
        municipality.is_active = False
        return self._repository.save(municipality)
