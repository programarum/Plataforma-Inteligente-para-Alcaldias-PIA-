"""Document and chunk HTTP routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.departments.infrastructure.repository import (
    SQLAlchemyDepartmentRepository,
)
from app.modules.documents.api.schemas import (
    DocumentChunkCreate,
    DocumentChunkResponse,
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate,
)
from app.modules.documents.application.service import (
    DocumentChunkService,
    DocumentService,
)
from app.modules.documents.infrastructure.repository import (
    SQLAlchemyDocumentChunkRepository,
    SQLAlchemyDocumentRepository,
)
from app.modules.municipalities.infrastructure.repository import (
    SQLAlchemyMunicipalityRepository,
)

router = APIRouter(prefix="/documents", tags=["Documents"])
DatabaseSession = Annotated[Session, Depends(get_db)]


def get_document_service(session: DatabaseSession) -> DocumentService:
    return DocumentService(
        SQLAlchemyDocumentRepository(session),
        SQLAlchemyMunicipalityRepository(session),
        SQLAlchemyDepartmentRepository(session),
    )


def get_chunk_service(session: DatabaseSession) -> DocumentChunkService:
    return DocumentChunkService(
        SQLAlchemyDocumentChunkRepository(session),
        SQLAlchemyDocumentRepository(session),
    )


DocumentServiceDependency = Annotated[DocumentService, Depends(get_document_service)]
ChunkServiceDependency = Annotated[DocumentChunkService, Depends(get_chunk_service)]


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document(
    payload: DocumentCreate, service: DocumentServiceDependency
) -> DocumentResponse:
    return DocumentResponse.model_validate(service.create(payload.to_command()))


@router.get("", response_model=list[DocumentResponse])
def list_documents(service: DocumentServiceDependency) -> list[DocumentResponse]:
    return [DocumentResponse.model_validate(item) for item in service.list()]


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: UUID, service: DocumentServiceDependency
) -> DocumentResponse:
    return DocumentResponse.model_validate(service.get(document_id))


@router.patch("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: UUID, payload: DocumentUpdate, service: DocumentServiceDependency
) -> DocumentResponse:
    return DocumentResponse.model_validate(
        service.update(document_id, payload.to_command())
    )


@router.patch("/{document_id}/archive", response_model=DocumentResponse)
def archive_document(
    document_id: UUID, service: DocumentServiceDependency
) -> DocumentResponse:
    return DocumentResponse.model_validate(service.archive(document_id))


@router.post(
    "/{document_id}/chunks",
    response_model=DocumentChunkResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_chunk(
    document_id: UUID,
    payload: DocumentChunkCreate,
    service: ChunkServiceDependency,
) -> DocumentChunkResponse:
    return DocumentChunkResponse.model_validate(
        service.create(document_id, payload.to_command())
    )


@router.get("/{document_id}/chunks", response_model=list[DocumentChunkResponse])
def list_chunks(
    document_id: UUID, service: ChunkServiceDependency
) -> list[DocumentChunkResponse]:
    return [
        DocumentChunkResponse.model_validate(chunk)
        for chunk in service.list(document_id)
    ]
