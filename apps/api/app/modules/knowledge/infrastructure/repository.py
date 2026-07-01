"""SQLAlchemy Knowledge Core repositories."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.knowledge.domain.models import KnowledgeItem, KnowledgeRelation


class SQLAlchemyKnowledgeItemRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, item: KnowledgeItem) -> KnowledgeItem:
        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        return item

    def list(self) -> list[KnowledgeItem]:
        statement = select(KnowledgeItem).order_by(KnowledgeItem.created_at)
        return list(self._session.scalars(statement))

    def get(self, item_id: UUID) -> KnowledgeItem | None:
        return self._session.get(KnowledgeItem, item_id)

    def save(self, item: KnowledgeItem) -> KnowledgeItem:
        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        return item


class SQLAlchemyKnowledgeRelationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, relation: KnowledgeRelation) -> KnowledgeRelation:
        self._session.add(relation)
        self._session.commit()
        self._session.refresh(relation)
        return relation

    def list_by_source(self, source_item_id: UUID) -> list[KnowledgeRelation]:
        statement = (
            select(KnowledgeRelation)
            .where(KnowledgeRelation.source_item_id == source_item_id)
            .order_by(KnowledgeRelation.created_at)
        )
        return list(self._session.scalars(statement))

