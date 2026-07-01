"""Reusable authentication and authorization dependencies."""

from collections.abc import Callable
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.application.service import AuthService
from app.modules.auth.domain.entities import AuthenticatedIdentity
from app.modules.auth.infrastructure.repository import SQLAlchemyAuthRepository
from app.shared.exceptions import AuthenticationError

bearer_scheme = HTTPBearer(auto_error=False)
DatabaseSession = Annotated[Session, Depends(get_db)]
BearerCredentials = Annotated[
    HTTPAuthorizationCredentials | None, Depends(bearer_scheme)
]


def get_auth_service(session: DatabaseSession) -> AuthService:
    return AuthService(SQLAlchemyAuthRepository(session))


AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]


def get_current_user(
    credentials: BearerCredentials, service: AuthServiceDependency
) -> AuthenticatedIdentity:
    """Resolve a valid bearer token to an active institutional identity."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationError("Bearer token required")
    return service.identity_from_token(credentials.credentials)


CurrentUser = Annotated[AuthenticatedIdentity, Depends(get_current_user)]


def require_active_user(identity: CurrentUser) -> AuthenticatedIdentity:
    """Require an active user; token resolution already enforces this invariant."""
    return identity


ActiveUser = Annotated[AuthenticatedIdentity, Depends(require_active_user)]


def require_superuser(identity: CurrentUser) -> AuthenticatedIdentity:
    """Require a superuser identity."""
    return AuthService.require_superuser(identity)


def require_permission(
    permission_code: str,
) -> Callable[[CurrentUser], AuthenticatedIdentity]:
    """Build a dependency that requires an effective RBAC permission."""

    def permission_dependency(identity: CurrentUser) -> AuthenticatedIdentity:
        return AuthService.require_permission(identity, permission_code)

    return permission_dependency
