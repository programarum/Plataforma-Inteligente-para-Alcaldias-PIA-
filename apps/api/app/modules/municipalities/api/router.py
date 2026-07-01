"""Municipality HTTP routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.municipalities.api.schemas import (
    MunicipalityCreate,
    MunicipalityResponse,
    MunicipalityUpdate,
)
from app.modules.municipalities.application.service import MunicipalityService
from app.modules.municipalities.infrastructure.repository import (
    SQLAlchemyMunicipalityRepository,
)

router = APIRouter(prefix="/municipalities", tags=["Municipalities"])
DatabaseSession = Annotated[Session, Depends(get_db)]


def get_service(session: DatabaseSession) -> MunicipalityService:
    return MunicipalityService(SQLAlchemyMunicipalityRepository(session))


MunicipalityServiceDependency = Annotated[MunicipalityService, Depends(get_service)]


@router.post(
    "", response_model=MunicipalityResponse, status_code=status.HTTP_201_CREATED
)
def create_municipality(
    payload: MunicipalityCreate, service: MunicipalityServiceDependency
) -> MunicipalityResponse:
    return MunicipalityResponse.model_validate(service.create(payload.to_command()))


@router.get("", response_model=list[MunicipalityResponse])
def list_municipalities(
    service: MunicipalityServiceDependency,
) -> list[MunicipalityResponse]:
    return [MunicipalityResponse.model_validate(item) for item in service.list()]


@router.get("/{municipality_id}", response_model=MunicipalityResponse)
def get_municipality(
    municipality_id: UUID, service: MunicipalityServiceDependency
) -> MunicipalityResponse:
    return MunicipalityResponse.model_validate(service.get(municipality_id))


@router.patch("/{municipality_id}", response_model=MunicipalityResponse)
def update_municipality(
    municipality_id: UUID,
    payload: MunicipalityUpdate,
    service: MunicipalityServiceDependency,
) -> MunicipalityResponse:
    result = service.update(municipality_id, payload.to_command())
    return MunicipalityResponse.model_validate(result)


@router.patch("/{municipality_id}/deactivate", response_model=MunicipalityResponse)
def deactivate_municipality(
    municipality_id: UUID, service: MunicipalityServiceDependency
) -> MunicipalityResponse:
    return MunicipalityResponse.model_validate(service.deactivate(municipality_id))
