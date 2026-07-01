"""Authenticated identity domain values."""

from dataclasses import dataclass

from app.modules.users.domain.models import User


@dataclass(frozen=True, slots=True)
class AuthenticatedIdentity:
    """A user enriched with resolved RBAC grants."""

    user: User
    roles: list[str]
    permissions: list[str]


@dataclass(frozen=True, slots=True)
class AccessToken:
    """Issued bearer token and its lifetime."""

    access_token: str
    token_type: str
    expires_in: int

