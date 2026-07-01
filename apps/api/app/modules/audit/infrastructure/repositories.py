"""SQLAlchemy repository implementation for audit records."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.audit.domain.entities import AuditLog
from app.modules.audit.infrastructure.models import AuditLogModel


class SqlAlchemyAuditLogRepository:
    """Persist audit records using a SQLAlchemy session."""

    def __init__(self, session: Session) -> None:
        """Initialize the repository with a unit-of-work session."""
        self._session = session

    def add(self, audit_log: AuditLog) -> AuditLog:
        """Persist and return an audit record."""
        model = AuditLogModel(
            id=audit_log.id,
            actor_id=audit_log.actor_id,
            action=audit_log.action,
            entity_type=audit_log.entity_type,
            entity_id=audit_log.entity_id,
            metadata_=audit_log.metadata,
            created_at=audit_log.created_at,
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def list(self) -> list[AuditLog]:
        """Return audit records in reverse chronological order."""
        statement = select(AuditLogModel).order_by(AuditLogModel.created_at.desc())
        models = self._session.scalars(statement).all()
        return [self._to_entity(model) for model in models]

    @staticmethod
    def _to_entity(model: AuditLogModel) -> AuditLog:
        """Map a persistence model to a domain entity."""
        return AuditLog(
            id=model.id,
            actor_id=model.actor_id,
            action=model.action,
            entity_type=model.entity_type,
            entity_id=model.entity_id,
            metadata=model.metadata_,
            created_at=model.created_at,
        )
