"""Permission use cases."""

from dataclasses import asdict
from uuid import UUID

from app.modules.permissions.application.dto import (
    CreatePermission,
    UpdatePermission,
)
from app.modules.permissions.domain.models import Permission
from app.modules.permissions.domain.repositories import PermissionRepository
from app.shared.exceptions import ConflictError, NotFoundError


class PermissionService:
    def __init__(self, repository: PermissionRepository) -> None:
        self._repository = repository

    def create(self, command: CreatePermission) -> Permission:
        code = command.code.lower()
        if self._repository.get_by_code(code) is not None:
            raise ConflictError("Permission code already exists")
        values = asdict(command)
        values["code"] = code
        return self._repository.add(Permission(**values))

    def list(self) -> list[Permission]:
        return self._repository.list()

    def get(self, permission_id: UUID) -> Permission:
        permission = self._repository.get(permission_id)
        if permission is None:
            raise NotFoundError("Permission not found")
        return permission

    def update(self, permission_id: UUID, command: UpdatePermission) -> Permission:
        permission = self.get(permission_id)
        values = asdict(command)
        if command.code is not None:
            values["code"] = command.code.lower()
            existing = self._repository.get_by_code(values["code"])
            if existing is not None and existing.id != permission.id:
                raise ConflictError("Permission code already exists")
        for name, value in values.items():
            if value is not None:
                setattr(permission, name, value)
        return self._repository.save(permission)

    def deactivate(self, permission_id: UUID) -> Permission:
        permission = self.get(permission_id)
        permission.is_active = False
        return self._repository.save(permission)

