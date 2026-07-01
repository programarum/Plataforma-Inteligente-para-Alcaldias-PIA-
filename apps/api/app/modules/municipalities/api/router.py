"""HTTP routes for municipality use cases."""

from typing import Annotated, NoReturn
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.modules.municipalities.api.schemas import (
    MunicipalityCreate,
    MunicipalityRead,
    MunicipalityUpdate,
)
from app.modules.municipalities.application.services import MunicipalityService
from app.modules.municipalities.infrastructure.repositories import (
    SqlAlchemyMunicipalityRepository,
)
from app.shared.exceptions import EntityNotFoundError

router = APIRouter(prefix="/municipalities")


def get_municipality_service(
    session: Annotated[Session, Depends(get_db_session)],
) -> MunicipalityService:
    """Build the municipality service for the current request."""
    return MunicipalityService(SqlAlchemyMunicipalityRepository(session))


MunicipalityServiceDependency = Annotated[
    MunicipalityService,
    Depends(get_municipality_service),
]


def raise_not_found(error: EntityNotFoundError) -> NoReturn:
    """Translate a domain lookup failure into an HTTP response."""
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.post("", response_model=MunicipalityRead, status_code=status.HTTP_201_CREATED)
def create_municipality(
    payload: MunicipalityCreate,
    service: MunicipalityServiceDependency,
) -> MunicipalityRead:
    """Create a municipality."""
    municipality = service.create(**payload.model_dump())
    return MunicipalityRead.model_validate(municipality)


@router.get("", response_model=list[MunicipalityRead])
def list_municipalities(service: MunicipalityServiceDependency) -> list[MunicipalityRead]:
    """List municipalities."""
    return [MunicipalityRead.model_validate(item) for item in service.list()]


@router.get("/{municipality_id}", response_model=MunicipalityRead)
def get_municipality(
    municipality_id: UUID,
    service: MunicipalityServiceDependency,
) -> MunicipalityRead:
    """Get one municipality by identifier."""
    try:
        municipality = service.get(municipality_id)
    except EntityNotFoundError as error:
        raise_not_found(error)
    return MunicipalityRead.model_validate(municipality)


@router.patch("/{municipality_id}", response_model=MunicipalityRead)
def update_municipality(
    municipality_id: UUID,
    payload: MunicipalityUpdate,
    service: MunicipalityServiceDependency,
) -> MunicipalityRead:
    """Partially update a municipality."""
    try:
        municipality = service.update(
            municipality_id,
            payload.model_dump(exclude_unset=True),
        )
    except EntityNotFoundError as error:
        raise_not_found(error)
    return MunicipalityRead.model_validate(municipality)


@router.patch("/{municipality_id}/deactivate", response_model=MunicipalityRead)
def deactivate_municipality(
    municipality_id: UUID,
    service: MunicipalityServiceDependency,
) -> MunicipalityRead:
    """Deactivate a municipality while retaining its history."""
    try:
        municipality = service.deactivate(municipality_id)
    except EntityNotFoundError as error:
        raise_not_found(error)
    return MunicipalityRead.model_validate(municipality)
