"""SQLAlchemy role repositories."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.permissions.domain.models import Permission
from app.modules.roles.domain.models import Role, RolePermission


class SQLAlchemyRoleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, role: Role) -> Role:
        self._session.add(role)
        self._session.commit()
        self._session.refresh(role)
        return role

    def list(self) -> list[Role]:
        return list(self._session.scalars(select(Role).order_by(Role.created_at)))

    def get(self, role_id: UUID) -> Role | None:
        return self._session.get(Role, role_id)

    def get_by_name(self, municipality_id: UUID, name: str) -> Role | None:
        statement = select(Role).where(
            Role.municipality_id == municipality_id, Role.name == name
        )
        return self._session.scalar(statement)

    def save(self, role: Role) -> Role:
        self._session.add(role)
        self._session.commit()
        self._session.refresh(role)
        return role


class SQLAlchemyRolePermissionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_assignment(
        self, role_id: UUID, permission_id: UUID
    ) -> RolePermission | None:
        statement = select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
        )
        return self._session.scalar(statement)

    def add(self, assignment: RolePermission) -> RolePermission:
        self._session.add(assignment)
        self._session.commit()
        self._session.refresh(assignment)
        return assignment

    def list_permissions(self, role_id: UUID) -> list[Permission]:
        statement = (
            select(Permission)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .where(RolePermission.role_id == role_id)
            .order_by(Permission.code)
        )
        return list(self._session.scalars(statement))

    def remove(self, assignment: RolePermission) -> None:
        self._session.delete(assignment)
        self._session.commit()

