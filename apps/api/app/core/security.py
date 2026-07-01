"""Security configuration boundary for future kernel functionality.

Authentication and authorization are intentionally out of scope for Sprint 2.
"""

from pydantic import SecretStr

from app.core.config import settings


def get_jwt_secret() -> SecretStr:
    """Return the configured signing secret without exposing its value."""
    return settings.jwt_secret

