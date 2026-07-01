"""Role and role-permission HTTP routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.municipalities.infrastructure.repository import (
    SQLAlchemyMunicipalityRepository,
)
from app.modules.permissions.api.schemas import PermissionResponse
from app.modules.permissions.infrastructure.repository import (
    SQLAlchemyPermissionRepository,
)
from app.modules.roles.api.schemas import (
    AssignPermissionRequest,
    RoleCreate,
    RolePermissionResponse,
    RoleResponse,
    RoleUpdate,
)
from app.modules.roles.application.service import RolePermissionService, RoleService
from app.modules.roles.infrastructure.repository import (
    SQLAlchemyRolePermissionRepository,
    SQLAlchemyRoleRepository,
)

router = APIRouter(prefix="/roles", tags=["Roles"])
DatabaseSession = Annotated[Session, Depends(get_db)]


def get_role_service(session: DatabaseSession) -> RoleService:
    return RoleService(
        SQLAlchemyRoleRepository(session), SQLAlchemyMunicipalityRepository(session)
    )


def get_role_permission_service(session: DatabaseSession) -> RolePermissionService:
    return RolePermissionService(
        SQLAlchemyRolePermissionRepository(session),
        SQLAlchemyRoleRepository(session),
        SQLAlchemyPermissionRepository(session),
    )


RoleServiceDependency = Annotated[RoleService, Depends(get_role_service)]
RolePermissionServiceDependency = Annotated[
    RolePermissionService, Depends(get_role_permission_service)
]


@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(payload: RoleCreate, service: RoleServiceDependency) -> RoleResponse:
    return RoleResponse.model_validate(service.create(payload.to_command()))


@router.get("", response_model=list[RoleResponse])
def list_roles(service: RoleServiceDependency) -> list[RoleResponse]:
    return [RoleResponse.model_validate(role) for role in service.list()]


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: UUID, service: RoleServiceDependency) -> RoleResponse:
    return RoleResponse.model_validate(service.get(role_id))


@router.patch("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: UUID, payload: RoleUpdate, service: RoleServiceDependency
) -> RoleResponse:
    return RoleResponse.model_validate(service.update(role_id, payload.to_command()))


@router.patch("/{role_id}/deactivate", response_model=RoleResponse)
def deactivate_role(role_id: UUID, service: RoleServiceDependency) -> RoleResponse:
    return RoleResponse.model_validate(service.deactivate(role_id))


@router.post(
    "/{role_id}/permissions",
    response_model=RolePermissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def assign_permission(
    role_id: UUID,
    payload: AssignPermissionRequest,
    service: RolePermissionServiceDependency,
) -> RolePermissionResponse:
    return RolePermissionResponse.model_validate(
        service.assign(role_id, payload.permission_id)
    )


@router.get("/{role_id}/permissions", response_model=list[PermissionResponse])
def list_role_permissions(
    role_id: UUID, service: RolePermissionServiceDependency
) -> list[PermissionResponse]:
    return [PermissionResponse.model_validate(item) for item in service.list(role_id)]


@router.delete(
    "/{role_id}/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT
)
def remove_permission(
    role_id: UUID,
    permission_id: UUID,
    service: RolePermissionServiceDependency,
) -> Response:
    service.remove(role_id, permission_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

