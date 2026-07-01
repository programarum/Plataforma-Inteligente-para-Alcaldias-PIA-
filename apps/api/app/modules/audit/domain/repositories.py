"""Repository contracts for audit records."""

from typing import Protocol

from app.modules.audit.domain.entities import AuditLog


class AuditLogRepository(Protocol):
    """Define persistence operations required by the audit module."""

    def add(self, audit_log: AuditLog) -> AuditLog:
        """Persist and return an audit record."""
        ...

    def list(self) -> list[AuditLog]:
        """Return audit records in reverse chronological order."""
        ...
