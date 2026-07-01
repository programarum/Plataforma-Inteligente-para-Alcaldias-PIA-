"""SQLAlchemy authentication repository."""

from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.modules.auth.domain.entities import AuthenticatedIdentity
from app.modules.permissions.domain.models import Permission
from app.modules.roles.domain.models import Role, RolePermission
from app.modules.users.domain.models import User, UserRole


class SQLAlchemyAuthRepository:
    """Resolve credentials and effective RBAC grants from SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def find_by_login(self, username_or_email: str) -> User | None:
        login = username_or_email.lower()
        statement = select(User).where(
            or_(User.username == login, User.email == login)
        )
        return self._session.scalar(statement)

    def get_user(self, user_id: UUID) -> User | None:
        return self._session.get(User, user_id)

    def get_identity(self, user: User) -> AuthenticatedIdentity:
        roles_statement = (
            select(Role.name)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user.id, Role.is_active.is_(True))
            .order_by(Role.name)
        )
        permissions_statement = (
            select(Permission.code)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(UserRole, UserRole.role_id == RolePermission.role_id)
            .join(Role, Role.id == UserRole.role_id)
            .where(
                UserRole.user_id == user.id,
                Role.is_active.is_(True),
                Permission.is_active.is_(True),
            )
            .distinct()
            .order_by(Permission.code)
        )
        return AuthenticatedIdentity(
            user=user,
            roles=list(self._session.scalars(roles_statement)),
            permissions=list(self._session.scalars(permissions_statement)),
        )

