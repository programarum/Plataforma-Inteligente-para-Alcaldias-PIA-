"""SQLAlchemy document repositories."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.documents.domain.models import Document, DocumentChunk


class SQLAlchemyDocumentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, document: Document) -> Document:
        self._session.add(document)
        self._session.commit()
        self._session.refresh(document)
        return document

    def list(self) -> list[Document]:
        statement = select(Document).order_by(Document.created_at)
        return list(self._session.scalars(statement))

    def get(self, document_id: UUID) -> Document | None:
        return self._session.get(Document, document_id)

    def save(self, document: Document) -> Document:
        self._session.add(document)
        self._session.commit()
        self._session.refresh(document)
        return document


class SQLAlchemyDocumentChunkRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, chunk: DocumentChunk) -> DocumentChunk:
        self._session.add(chunk)
        self._session.commit()
        self._session.refresh(chunk)
        return chunk

    def list_by_document(self, document_id: UUID) -> list[DocumentChunk]:
        statement = (
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        )
        return list(self._session.scalars(statement))
