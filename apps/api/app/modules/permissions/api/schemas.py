"""Permission HTTP schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.permissions.application.dto import (
    CreatePermission,
    UpdatePermission,
)


class PermissionCreate(BaseModel):
    code: str = Field(min_length=3, max_length=150, pattern=r"^[a-zA-Z0-9._:-]+$")
    name: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1)
    module: str = Field(min_length=1, max_length=100)
    action: str = Field(min_length=1, max_length=100)
    is_active: bool = True

    def to_command(self) -> CreatePermission:
        return CreatePermission(**self.model_dump())


class PermissionUpdate(BaseModel):
    code: str | None = Field(
        default=None, min_length=3, max_length=150, pattern=r"^[a-zA-Z0-9._:-]+$"
    )
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1)
    module: str | None = Field(default=None, min_length=1, max_length=100)
    action: str | None = Field(default=None, min_length=1, max_length=100)

    def to_command(self) -> UpdatePermission:
        return UpdatePermission(**self.model_dump())


class PermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    name: str
    description: str
    module: str
    action: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

