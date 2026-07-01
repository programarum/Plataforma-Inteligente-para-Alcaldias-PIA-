"""Role HTTP schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.roles.application.dto import CreateRole, UpdateRole


class RoleCreate(BaseModel):
    municipality_id: UUID
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    is_system: bool = False
    is_active: bool = True

    def to_command(self) -> CreateRole:
        return CreateRole(**self.model_dump())


class RoleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1)

    def to_command(self) -> UpdateRole:
        return UpdateRole(**self.model_dump())


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    municipality_id: UUID
    name: str
    description: str
    is_system: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AssignPermissionRequest(BaseModel):
    permission_id: UUID


class RolePermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    role_id: UUID
    permission_id: UUID
    created_at: datetime

