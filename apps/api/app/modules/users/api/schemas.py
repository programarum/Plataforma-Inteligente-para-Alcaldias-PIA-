"""User HTTP schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.modules.users.application.dto import CreateUser, UpdateUser


class UserCreate(BaseModel):
    municipality_id: UUID
    department_id: UUID | None = None
    full_name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    username: str = Field(min_length=3, max_length=100, pattern=r"^[a-zA-Z0-9._-]+$")
    password: str = Field(min_length=12, max_length=128)
    phone: str | None = Field(default=None, max_length=50)
    position: str | None = Field(default=None, max_length=150)
    is_active: bool = True
    is_superuser: bool = False

    def to_command(self) -> CreateUser:
        return CreateUser(**self.model_dump())


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    email: EmailStr | None = None
    username: str | None = Field(
        default=None, min_length=3, max_length=100, pattern=r"^[a-zA-Z0-9._-]+$"
    )
    phone: str | None = Field(default=None, max_length=50)
    position: str | None = Field(default=None, max_length=150)

    def to_command(self) -> UpdateUser:
        return UpdateUser(**self.model_dump())


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    municipality_id: UUID
    department_id: UUID | None
    full_name: str
    email: EmailStr
    username: str
    phone: str | None
    position: str | None
    is_active: bool
    is_superuser: bool
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime


class AssignRoleRequest(BaseModel):
    role_id: UUID


class UserRoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    role_id: UUID
    created_at: datetime
