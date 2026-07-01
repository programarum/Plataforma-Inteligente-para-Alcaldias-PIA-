"""Authentication repository port."""

from typing import Protocol
from uuid import UUID

from app.modules.auth.domain.entities import AuthenticatedIdentity
from app.modules.users.domain.models import User


class AuthRepository(Protocol):
    def find_by_login(self, username_or_email: str) -> User | None: ...
    def get_user(self, user_id: UUID) -> User | None: ...
    def get_identity(self, user: User) -> AuthenticatedIdentity: ...

