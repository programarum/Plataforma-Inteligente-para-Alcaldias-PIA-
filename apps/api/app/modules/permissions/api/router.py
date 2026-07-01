"""Permission HTTP routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.permissions.api.schemas import (
    PermissionCreate,
    PermissionResponse,
    PermissionUpdate,
)
from app.modules.permissions.application.service import PermissionService
from app.modules.permissions.infrastructure.repository import (
    SQLAlchemyPermissionRepository,
)

router = APIRouter(prefix="/permissions", tags=["Permissions"])
DatabaseSession = Annotated[Session, Depends(get_db)]


def get_service(session: DatabaseSession) -> PermissionService:
    return PermissionService(SQLAlchemyPermissionRepository(session))


PermissionServiceDependency = Annotated[PermissionService, Depends(get_service)]


@router.post("", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
def create_permission(
    payload: PermissionCreate, service: PermissionServiceDependency
) -> PermissionResponse:
    return PermissionResponse.model_validate(service.create(payload.to_command()))


@router.get("", response_model=list[PermissionResponse])
def list_permissions(
    service: PermissionServiceDependency,
) -> list[PermissionResponse]:
    return [PermissionResponse.model_validate(item) for item in service.list()]


@router.get("/{permission_id}", response_model=PermissionResponse)
def get_permission(
    permission_id: UUID, service: PermissionServiceDependency
) -> PermissionResponse:
    return PermissionResponse.model_validate(service.get(permission_id))


@router.patch("/{permission_id}", response_model=PermissionResponse)
def update_permission(
    permission_id: UUID,
    payload: PermissionUpdate,
    service: PermissionServiceDependency,
) -> PermissionResponse:
    return PermissionResponse.model_validate(
        service.update(permission_id, payload.to_command())
    )


@router.patch("/{permission_id}/deactivate", response_model=PermissionResponse)
def deactivate_permission(
    permission_id: UUID, service: PermissionServiceDependency
) -> PermissionResponse:
    return PermissionResponse.model_validate(service.deactivate(permission_id))

