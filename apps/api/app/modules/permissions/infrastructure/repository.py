"""SQLAlchemy permission repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.permissions.domain.models import Permission


class SQLAlchemyPermissionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, permission: Permission) -> Permission:
        self._session.add(permission)
        self._session.commit()
        self._session.refresh(permission)
        return permission

    def list(self) -> list[Permission]:
        statement = select(Permission).order_by(Permission.created_at)
        return list(self._session.scalars(statement))

    def get(self, permission_id: UUID) -> Permission | None:
        return self._session.get(Permission, permission_id)

    def get_by_code(self, code: str) -> Permission | None:
        return self._session.scalar(select(Permission).where(Permission.code == code))

    def save(self, permission: Permission) -> Permission:
        self._session.add(permission)
        self._session.commit()
        self._session.refresh(permission)
        return permission

