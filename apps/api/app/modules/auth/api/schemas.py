"""Authentication HTTP schemas."""

from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.modules.auth.domain.entities import AuthenticatedIdentity


class LoginRequest(BaseModel):
    username_or_email: str = Field(min_length=1, max_length=320)
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class CurrentUserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    username: str
    municipality_id: UUID
    department_id: UUID | None
    roles: list[str]
    permissions: list[str]
    is_superuser: bool

    @classmethod
    def from_identity(cls, identity: AuthenticatedIdentity) -> "CurrentUserResponse":
        user = identity.user
        return cls(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            username=user.username,
            municipality_id=user.municipality_id,
            department_id=user.department_id,
            roles=identity.roles,
            permissions=identity.permissions,
            is_superuser=user.is_superuser,
        )

