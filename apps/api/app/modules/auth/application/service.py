"""Authentication and RBAC use cases."""

from uuid import UUID

from app.core.security import (
    TokenError,
    create_access_token,
    decode_access_token,
    verify_password,
)
from app.modules.auth.domain.entities import AccessToken, AuthenticatedIdentity
from app.modules.auth.domain.repositories import AuthRepository
from app.shared.exceptions import AuthenticationError, AuthorizationError


class AuthService:
    """Authenticate credentials and resolve JWT-backed identities."""

    def __init__(self, repository: AuthRepository) -> None:
        self._repository = repository

    def login(self, username_or_email: str, password: str) -> AccessToken:
        user = self._repository.find_by_login(username_or_email)
        if user is None or not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid username/email or password")
        if not user.is_active:
            raise AuthenticationError("Inactive user")
        token, expires_in = create_access_token(str(user.id))
        return AccessToken(token, "bearer", expires_in)

    def identity_from_token(self, token: str) -> AuthenticatedIdentity:
        try:
            claims = decode_access_token(token)
            subject = claims.get("sub")
            if not isinstance(subject, str):
                raise TokenError("Missing token subject")
            user_id = UUID(subject)
        except (TokenError, ValueError) as exc:
            raise AuthenticationError() from exc
        user = self._repository.get_user(user_id)
        if user is None or not user.is_active:
            raise AuthenticationError()
        return self._repository.get_identity(user)

    @staticmethod
    def require_superuser(identity: AuthenticatedIdentity) -> AuthenticatedIdentity:
        if not identity.user.is_superuser:
            raise AuthorizationError("Superuser access required")
        return identity

    @staticmethod
    def require_permission(
        identity: AuthenticatedIdentity, permission_code: str
    ) -> AuthenticatedIdentity:
        if (
            not identity.user.is_superuser
            and permission_code not in identity.permissions
        ):
            raise AuthorizationError()
        return identity
