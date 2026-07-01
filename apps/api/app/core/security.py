"""Security configuration boundary for future kernel functionality.

Authentication and authorization are intentionally out of scope for Sprint 2.
"""

from pwdlib import PasswordHash
from pydantic import SecretStr

from app.core.config import settings

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a password with the recommended Argon2 configuration."""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a stored hash for future authentication."""
    return password_hasher.verify(password, password_hash)


def get_jwt_secret() -> SecretStr:
    """Return the configured signing secret without exposing its value."""
    return settings.jwt_secret
