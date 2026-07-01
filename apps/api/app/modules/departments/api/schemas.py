"""Department HTTP request and response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.departments.application.dto import CreateDepartment, UpdateDepartment


class DepartmentCreate(BaseModel):
    municipality_id: UUID
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    manager_name: str = Field(min_length=1, max_length=200)
    is_active: bool = True

    def to_command(self) -> CreateDepartment:
        return CreateDepartment(**self.model_dump())


class DepartmentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1)
    manager_name: str | None = Field(default=None, min_length=1, max_length=200)

    def to_command(self) -> UpdateDepartment:
        return UpdateDepartment(**self.model_dump())


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    municipality_id: UUID
    name: str
    description: str
    manager_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

