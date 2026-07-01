"""Password hashing and JWT security primitives."""

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import SecretStr

from app.core.config import settings

password_hasher = PasswordHash.recommended()


class TokenError(ValueError):
    """Raised when a JWT cannot be trusted."""


def get_password_hash(password: str) -> str:
    """Hash a password with the recommended Argon2 configuration."""
    return password_hasher.hash(password)


def hash_password(password: str) -> str:
    """Backward-compatible password hashing alias."""
    return get_password_hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a stored hash for future authentication."""
    return password_hasher.verify(password, password_hash)


def get_jwt_secret() -> SecretStr:
    """Return the configured signing secret without exposing its value."""
    return settings.jwt_secret


def create_access_token(
    subject: str, expires_delta: timedelta | None = None
) -> tuple[str, int]:
    """Create a signed access token and return it with its lifetime in seconds."""
    lifetime = expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    now = datetime.now(UTC)
    expires_at = now + lifetime
    claims = {"sub": subject, "iat": now, "exp": expires_at}
    token = jwt.encode(
        claims,
        settings.jwt_secret.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )
    return token, int(lifetime.total_seconds())


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a signed access token, including expiration."""
    try:
        return jwt.decode(
            token,
            settings.jwt_secret.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
        )
    except InvalidTokenError as exc:
        raise TokenError("Invalid or expired access token") from exc
