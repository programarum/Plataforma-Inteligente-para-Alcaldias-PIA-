"""Role and role-permission use cases."""

from dataclasses import asdict
from uuid import UUID

from app.modules.municipalities.domain.repositories import MunicipalityRepository
from app.modules.permissions.domain.models import Permission
from app.modules.permissions.domain.repositories import PermissionRepository
from app.modules.roles.application.dto import CreateRole, UpdateRole
from app.modules.roles.domain.models import Role, RolePermission
from app.modules.roles.domain.repositories import (
    RolePermissionRepository,
    RoleRepository,
)
from app.shared.exceptions import ConflictError, NotFoundError


class RoleService:
    def __init__(
        self, repository: RoleRepository, municipalities: MunicipalityRepository
    ) -> None:
        self._repository = repository
        self._municipalities = municipalities

    def create(self, command: CreateRole) -> Role:
        if self._municipalities.get(command.municipality_id) is None:
            raise NotFoundError("Municipality not found")
        if (
            self._repository.get_by_name(command.municipality_id, command.name)
            is not None
        ):
            raise ConflictError("Role name already exists in municipality")
        return self._repository.add(Role(**asdict(command)))

    def list(self) -> list[Role]:
        return self._repository.list()

    def get(self, role_id: UUID) -> Role:
        role = self._repository.get(role_id)
        if role is None:
            raise NotFoundError("Role not found")
        return role

    def update(self, role_id: UUID, command: UpdateRole) -> Role:
        role = self.get(role_id)
        if command.name is not None:
            existing = self._repository.get_by_name(role.municipality_id, command.name)
            if existing is not None and existing.id != role.id:
                raise ConflictError("Role name already exists in municipality")
        for name, value in asdict(command).items():
            if value is not None:
                setattr(role, name, value)
        return self._repository.save(role)

    def deactivate(self, role_id: UUID) -> Role:
        role = self.get(role_id)
        role.is_active = False
        return self._repository.save(role)


class RolePermissionService:
    def __init__(
        self,
        assignments: RolePermissionRepository,
        roles: RoleRepository,
        permissions: PermissionRepository,
    ) -> None:
        self._assignments = assignments
        self._roles = roles
        self._permissions = permissions

    def assign(self, role_id: UUID, permission_id: UUID) -> RolePermission:
        if self._roles.get(role_id) is None:
            raise NotFoundError("Role not found")
        if self._permissions.get(permission_id) is None:
            raise NotFoundError("Permission not found")
        if self._assignments.get_assignment(role_id, permission_id) is not None:
            raise ConflictError("Permission already assigned to role")
        return self._assignments.add(
            RolePermission(role_id=role_id, permission_id=permission_id)
        )

    def list(self, role_id: UUID) -> list[Permission]:
        if self._roles.get(role_id) is None:
            raise NotFoundError("Role not found")
        return self._assignments.list_permissions(role_id)

    def remove(self, role_id: UUID, permission_id: UUID) -> None:
        assignment = self._assignments.get_assignment(role_id, permission_id)
        if assignment is None:
            raise NotFoundError("Role permission assignment not found")
        self._assignments.remove(assignment)
