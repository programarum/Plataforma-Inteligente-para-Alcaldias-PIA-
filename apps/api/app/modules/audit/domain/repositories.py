"""Audit repository port."""

from typing import Protocol
from uuid import UUID

from app.modules.audit.domain.models import AuditLog


class AuditLogRepository(Protocol):
    """Persistence operations currently required for audit logs."""

    def add(self, audit_log: AuditLog) -> AuditLog: ...

    def get(self, audit_log_id: UUID) -> AuditLog | None: ...

