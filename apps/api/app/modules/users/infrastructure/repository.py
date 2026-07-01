"""SQLAlchemy user repositories."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.roles.domain.models import Role
from app.modules.users.domain.models import User, UserRole


class SQLAlchemyUserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, user: User) -> User:
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def list(self) -> list[User]:
        return list(self._session.scalars(select(User).order_by(User.created_at)))

    def get(self, user_id: UUID) -> User | None:
        return self._session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self._session.scalar(select(User).where(User.email == email))

    def get_by_username(self, username: str) -> User | None:
        return self._session.scalar(select(User).where(User.username == username))

    def save(self, user: User) -> User:
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user


class SQLAlchemyUserRoleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_assignment(self, user_id: UUID, role_id: UUID) -> UserRole | None:
        statement = select(UserRole).where(
            UserRole.user_id == user_id, UserRole.role_id == role_id
        )
        return self._session.scalar(statement)

    def add(self, assignment: UserRole) -> UserRole:
        self._session.add(assignment)
        self._session.commit()
        self._session.refresh(assignment)
        return assignment

    def list_roles(self, user_id: UUID) -> list[Role]:
        statement = (
            select(Role)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
            .order_by(Role.name)
        )
        return list(self._session.scalars(statement))

    def remove(self, assignment: UserRole) -> None:
        self._session.delete(assignment)
        self._session.commit()

