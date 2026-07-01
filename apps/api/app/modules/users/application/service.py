"""User and user-role use cases."""

from dataclasses import asdict
from uuid import UUID

from app.core.security import hash_password
from app.modules.departments.domain.repositories import DepartmentRepository
from app.modules.municipalities.domain.repositories import MunicipalityRepository
from app.modules.roles.domain.models import Role
from app.modules.roles.domain.repositories import RoleRepository
from app.modules.users.application.dto import CreateUser, UpdateUser
from app.modules.users.domain.models import User, UserRole
from app.modules.users.domain.repositories import UserRepository, UserRoleRepository
from app.shared.exceptions import ConflictError, NotFoundError


class UserService:
    def __init__(
        self,
        repository: UserRepository,
        municipalities: MunicipalityRepository,
        departments: DepartmentRepository,
    ) -> None:
        self._repository = repository
        self._municipalities = municipalities
        self._departments = departments

    def create(self, command: CreateUser) -> User:
        if self._municipalities.get(command.municipality_id) is None:
            raise NotFoundError("Municipality not found")
        if command.department_id is not None:
            department = self._departments.get(command.department_id)
            if (
                department is None
                or department.municipality_id != command.municipality_id
            ):
                raise NotFoundError("Department not found for municipality")
        email = command.email.lower()
        username = command.username.lower()
        if self._repository.get_by_email(email) is not None:
            raise ConflictError("Email already exists")
        if self._repository.get_by_username(username) is not None:
            raise ConflictError("Username already exists")
        values = asdict(command)
        password = values.pop("password")
        values.update(
            email=email,
            username=username,
            password_hash=hash_password(password),
        )
        return self._repository.add(User(**values))

    def list(self) -> list[User]:
        return self._repository.list()

    def get(self, user_id: UUID) -> User:
        user = self._repository.get(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return user

    def update(self, user_id: UUID, command: UpdateUser) -> User:
        user = self.get(user_id)
        values = asdict(command)
        if command.email is not None:
            values["email"] = command.email.lower()
            existing = self._repository.get_by_email(values["email"])
            if existing is not None and existing.id != user.id:
                raise ConflictError("Email already exists")
        if command.username is not None:
            values["username"] = command.username.lower()
            existing = self._repository.get_by_username(values["username"])
            if existing is not None and existing.id != user.id:
                raise ConflictError("Username already exists")
        for name, value in values.items():
            if value is not None:
                setattr(user, name, value)
        return self._repository.save(user)

    def deactivate(self, user_id: UUID) -> User:
        user = self.get(user_id)
        user.is_active = False
        return self._repository.save(user)


class UserRoleService:
    def __init__(
        self,
        assignments: UserRoleRepository,
        users: UserRepository,
        roles: RoleRepository,
    ) -> None:
        self._assignments = assignments
        self._users = users
        self._roles = roles

    def assign(self, user_id: UUID, role_id: UUID) -> UserRole:
        user = self._users.get(user_id)
        if user is None:
            raise NotFoundError("User not found")
        role = self._roles.get(role_id)
        if role is None:
            raise NotFoundError("Role not found")
        if role.municipality_id != user.municipality_id:
            raise ConflictError("Role and user must belong to the same municipality")
        if self._assignments.get_assignment(user_id, role_id) is not None:
            raise ConflictError("Role already assigned to user")
        return self._assignments.add(UserRole(user_id=user_id, role_id=role_id))

    def list(self, user_id: UUID) -> list[Role]:
        if self._users.get(user_id) is None:
            raise NotFoundError("User not found")
        return self._assignments.list_roles(user_id)

    def remove(self, user_id: UUID, role_id: UUID) -> None:
        assignment = self._assignments.get_assignment(user_id, role_id)
        if assignment is None:
            raise NotFoundError("User role assignment not found")
        self._assignments.remove(assignment)
