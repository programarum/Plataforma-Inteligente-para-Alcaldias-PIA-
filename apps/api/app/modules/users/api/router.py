"""User and user-role HTTP routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.departments.infrastructure.repository import (
    SQLAlchemyDepartmentRepository,
)
from app.modules.municipalities.infrastructure.repository import (
    SQLAlchemyMunicipalityRepository,
)
from app.modules.roles.api.schemas import RoleResponse
from app.modules.roles.infrastructure.repository import SQLAlchemyRoleRepository
from app.modules.users.api.schemas import (
    AssignRoleRequest,
    UserCreate,
    UserResponse,
    UserRoleResponse,
    UserUpdate,
)
from app.modules.users.application.service import UserRoleService, UserService
from app.modules.users.infrastructure.repository import (
    SQLAlchemyUserRepository,
    SQLAlchemyUserRoleRepository,
)

router = APIRouter(prefix="/users", tags=["Users"])
DatabaseSession = Annotated[Session, Depends(get_db)]


def get_user_service(session: DatabaseSession) -> UserService:
    return UserService(
        SQLAlchemyUserRepository(session),
        SQLAlchemyMunicipalityRepository(session),
        SQLAlchemyDepartmentRepository(session),
    )


def get_user_role_service(session: DatabaseSession) -> UserRoleService:
    return UserRoleService(
        SQLAlchemyUserRoleRepository(session),
        SQLAlchemyUserRepository(session),
        SQLAlchemyRoleRepository(session),
    )


UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
UserRoleServiceDependency = Annotated[UserRoleService, Depends(get_user_role_service)]


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, service: UserServiceDependency) -> UserResponse:
    return UserResponse.model_validate(service.create(payload.to_command()))


@router.get("", response_model=list[UserResponse])
def list_users(service: UserServiceDependency) -> list[UserResponse]:
    return [UserResponse.model_validate(user) for user in service.list()]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, service: UserServiceDependency) -> UserResponse:
    return UserResponse.model_validate(service.get(user_id))


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID, payload: UserUpdate, service: UserServiceDependency
) -> UserResponse:
    return UserResponse.model_validate(service.update(user_id, payload.to_command()))


@router.patch("/{user_id}/deactivate", response_model=UserResponse)
def deactivate_user(user_id: UUID, service: UserServiceDependency) -> UserResponse:
    return UserResponse.model_validate(service.deactivate(user_id))


@router.post(
    "/{user_id}/roles",
    response_model=UserRoleResponse,
    status_code=status.HTTP_201_CREATED,
)
def assign_role(
    user_id: UUID, payload: AssignRoleRequest, service: UserRoleServiceDependency
) -> UserRoleResponse:
    return UserRoleResponse.model_validate(service.assign(user_id, payload.role_id))


@router.get("/{user_id}/roles", response_model=list[RoleResponse])
def list_user_roles(
    user_id: UUID, service: UserRoleServiceDependency
) -> list[RoleResponse]:
    return [RoleResponse.model_validate(role) for role in service.list(user_id)]


@router.delete("/{user_id}/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_role(
    user_id: UUID, role_id: UUID, service: UserRoleServiceDependency
) -> Response:
    service.remove(user_id, role_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

