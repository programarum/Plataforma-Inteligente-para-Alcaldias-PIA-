"""SQLAlchemy audit log repository."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.audit.domain.models import AuditLog


class SQLAlchemyAuditLogRepository:
    """Persist append-only audit records."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, audit_log: AuditLog) -> AuditLog:
        self._session.add(audit_log)
        self._session.commit()
        self._session.refresh(audit_log)
        return audit_log

    def get(self, audit_log_id: UUID) -> AuditLog | None:
        return self._session.get(AuditLog, audit_log_id)

