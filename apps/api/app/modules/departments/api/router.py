"""Department HTTP routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.departments.api.schemas import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
)
from app.modules.departments.application.service import DepartmentService
from app.modules.departments.infrastructure.repository import (
    SQLAlchemyDepartmentRepository,
)
from app.modules.municipalities.infrastructure.repository import (
    SQLAlchemyMunicipalityRepository,
)

router = APIRouter(prefix="/departments", tags=["Departments"])
DatabaseSession = Annotated[Session, Depends(get_db)]


def get_service(session: DatabaseSession) -> DepartmentService:
    return DepartmentService(
        SQLAlchemyDepartmentRepository(session),
        SQLAlchemyMunicipalityRepository(session),
    )


DepartmentServiceDependency = Annotated[DepartmentService, Depends(get_service)]


@router.post("", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
    payload: DepartmentCreate, service: DepartmentServiceDependency
) -> DepartmentResponse:
    return DepartmentResponse.model_validate(service.create(payload.to_command()))


@router.get("", response_model=list[DepartmentResponse])
def list_departments(
    service: DepartmentServiceDependency,
) -> list[DepartmentResponse]:
    return [DepartmentResponse.model_validate(item) for item in service.list()]


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: UUID, service: DepartmentServiceDependency
) -> DepartmentResponse:
    return DepartmentResponse.model_validate(service.get(department_id))


@router.patch("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: UUID,
    payload: DepartmentUpdate,
    service: DepartmentServiceDependency,
) -> DepartmentResponse:
    result = service.update(department_id, payload.to_command())
    return DepartmentResponse.model_validate(result)


@router.patch("/{department_id}/deactivate", response_model=DepartmentResponse)
def deactivate_department(
    department_id: UUID, service: DepartmentServiceDependency
) -> DepartmentResponse:
    return DepartmentResponse.model_validate(service.deactivate(department_id))

