"""Document and chunk use cases."""

from dataclasses import asdict
from uuid import UUID

from app.modules.departments.domain.repositories import DepartmentRepository
from app.modules.documents.application.dto import (
    CreateDocument,
    CreateDocumentChunk,
    UpdateDocument,
)
from app.modules.documents.domain.models import Document, DocumentChunk
from app.modules.documents.domain.repositories import (
    DocumentChunkRepository,
    DocumentRepository,
)
from app.modules.municipalities.domain.repositories import MunicipalityRepository
from app.shared.exceptions import NotFoundError


class DocumentService:
    def __init__(
        self,
        repository: DocumentRepository,
        municipality_repository: MunicipalityRepository,
        department_repository: DepartmentRepository,
    ) -> None:
        self._repository = repository
        self._municipalities = municipality_repository
        self._departments = department_repository

    def create(self, command: CreateDocument) -> Document:
        if self._municipalities.get(command.municipality_id) is None:
            raise NotFoundError("Municipality not found")
        department = self._departments.get(command.department_id)
        if department is None or department.municipality_id != command.municipality_id:
            raise NotFoundError("Department not found for municipality")
        return self._repository.add(Document(**asdict(command)))

    def list(self) -> list[Document]:
        return self._repository.list()

    def get(self, document_id: UUID) -> Document:
        document = self._repository.get(document_id)
        if document is None:
            raise NotFoundError("Document not found")
        return document

    def update(self, document_id: UUID, command: UpdateDocument) -> Document:
        document = self.get(document_id)
        for name, value in asdict(command).items():
            if value is not None:
                setattr(document, name, value)
        return self._repository.save(document)

    def archive(self, document_id: UUID) -> Document:
        document = self.get(document_id)
        document.status = "archived"
        return self._repository.save(document)


class DocumentChunkService:
    def __init__(
        self, repository: DocumentChunkRepository, documents: DocumentRepository
    ) -> None:
        self._repository = repository
        self._documents = documents

    def create(
        self, document_id: UUID, command: CreateDocumentChunk
    ) -> DocumentChunk:
        if self._documents.get(document_id) is None:
            raise NotFoundError("Document not found")
        values = asdict(command)
        values["metadata_"] = values.pop("metadata")
        return self._repository.add(DocumentChunk(document_id=document_id, **values))

    def list(self, document_id: UUID) -> list[DocumentChunk]:
        if self._documents.get(document_id) is None:
            raise NotFoundError("Document not found")
        return self._repository.list_by_document(document_id)

