"""HTTP routes for department use cases."""

from typing import Annotated, NoReturn
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.modules.departments.api.schemas import (
    DepartmentCreate,
    DepartmentRead,
    DepartmentUpdate,
)
from app.modules.departments.application.services import DepartmentService
from app.modules.departments.infrastructure.repositories import (
    SqlAlchemyDepartmentRepository,
)
from app.modules.municipalities.infrastructure.repositories import (
    SqlAlchemyMunicipalityRepository,
)
from app.shared.exceptions import EntityNotFoundError

router = APIRouter(prefix="/departments")


def get_department_service(
    session: Annotated[Session, Depends(get_db_session)],
) -> DepartmentService:
    """Build the department service for the current request."""
    return DepartmentService(
        SqlAlchemyDepartmentRepository(session),
        SqlAlchemyMunicipalityRepository(session),
    )


DepartmentServiceDependency = Annotated[
    DepartmentService,
    Depends(get_department_service),
]


def raise_not_found(error: EntityNotFoundError) -> NoReturn:
    """Translate a domain lookup failure into an HTTP response."""
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.post("", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
def create_department(
    payload: DepartmentCreate,
    service: DepartmentServiceDependency,
) -> DepartmentRead:
    """Create a municipal department."""
    try:
        department = service.create(**payload.model_dump())
    except EntityNotFoundError as error:
        raise_not_found(error)
    return DepartmentRead.model_validate(department)


@router.get("", response_model=list[DepartmentRead])
def list_departments(service: DepartmentServiceDependency) -> list[DepartmentRead]:
    """List municipal departments."""
    return [DepartmentRead.model_validate(item) for item in service.list()]


@router.get("/{department_id}", response_model=DepartmentRead)
def get_department(
    department_id: UUID,
    service: DepartmentServiceDependency,
) -> DepartmentRead:
    """Get one municipal department by identifier."""
    try:
        department = service.get(department_id)
    except EntityNotFoundError as error:
        raise_not_found(error)
    return DepartmentRead.model_validate(department)


@router.patch("/{department_id}", response_model=DepartmentRead)
def update_department(
    department_id: UUID,
    payload: DepartmentUpdate,
    service: DepartmentServiceDependency,
) -> DepartmentRead:
    """Partially update a municipal department."""
    try:
        department = service.update(
            department_id,
            payload.model_dump(exclude_unset=True),
        )
    except EntityNotFoundError as error:
        raise_not_found(error)
    return DepartmentRead.model_validate(department)


@router.patch("/{department_id}/deactivate", response_model=DepartmentRead)
def deactivate_department(
    department_id: UUID,
    service: DepartmentServiceDependency,
) -> DepartmentRead:
    """Deactivate a department while retaining its history."""
    try:
        department = service.deactivate(department_id)
    except EntityNotFoundError as error:
        raise_not_found(error)
    return DepartmentRead.model_validate(department)
