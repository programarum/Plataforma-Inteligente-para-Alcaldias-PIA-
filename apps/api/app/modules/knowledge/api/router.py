"""Knowledge item and relation HTTP routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.departments.infrastructure.repository import (
    SQLAlchemyDepartmentRepository,
)
from app.modules.documents.infrastructure.repository import SQLAlchemyDocumentRepository
from app.modules.knowledge.api.schemas import (
    KnowledgeItemCreate,
    KnowledgeItemResponse,
    KnowledgeItemUpdate,
    KnowledgeRelationCreate,
    KnowledgeRelationResponse,
)
from app.modules.knowledge.application.service import (
    KnowledgeItemService,
    KnowledgeRelationService,
)
from app.modules.knowledge.infrastructure.repository import (
    SQLAlchemyKnowledgeItemRepository,
    SQLAlchemyKnowledgeRelationRepository,
)
from app.modules.municipalities.infrastructure.repository import (
    SQLAlchemyMunicipalityRepository,
)

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])
DatabaseSession = Annotated[Session, Depends(get_db)]


def get_item_service(session: DatabaseSession) -> KnowledgeItemService:
    return KnowledgeItemService(
        SQLAlchemyKnowledgeItemRepository(session),
        SQLAlchemyMunicipalityRepository(session),
        SQLAlchemyDepartmentRepository(session),
        SQLAlchemyDocumentRepository(session),
    )


def get_relation_service(session: DatabaseSession) -> KnowledgeRelationService:
    return KnowledgeRelationService(
        SQLAlchemyKnowledgeRelationRepository(session),
        SQLAlchemyKnowledgeItemRepository(session),
    )


ItemServiceDependency = Annotated[KnowledgeItemService, Depends(get_item_service)]
RelationServiceDependency = Annotated[
    KnowledgeRelationService, Depends(get_relation_service)
]


@router.post(
    "/items",
    response_model=KnowledgeItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_item(
    payload: KnowledgeItemCreate, service: ItemServiceDependency
) -> KnowledgeItemResponse:
    return KnowledgeItemResponse.model_validate(service.create(payload.to_command()))


@router.get("/items", response_model=list[KnowledgeItemResponse])
def list_items(service: ItemServiceDependency) -> list[KnowledgeItemResponse]:
    return [KnowledgeItemResponse.model_validate(item) for item in service.list()]


@router.get("/items/{item_id}", response_model=KnowledgeItemResponse)
def get_item(item_id: UUID, service: ItemServiceDependency) -> KnowledgeItemResponse:
    return KnowledgeItemResponse.model_validate(service.get(item_id))


@router.patch("/items/{item_id}", response_model=KnowledgeItemResponse)
def update_item(
    item_id: UUID, payload: KnowledgeItemUpdate, service: ItemServiceDependency
) -> KnowledgeItemResponse:
    return KnowledgeItemResponse.model_validate(
        service.update(item_id, payload.to_command())
    )


@router.patch("/items/{item_id}/archive", response_model=KnowledgeItemResponse)
def archive_item(
    item_id: UUID, service: ItemServiceDependency
) -> KnowledgeItemResponse:
    return KnowledgeItemResponse.model_validate(service.archive(item_id))


@router.post(
    "/relations",
    response_model=KnowledgeRelationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_relation(
    payload: KnowledgeRelationCreate, service: RelationServiceDependency
) -> KnowledgeRelationResponse:
    return KnowledgeRelationResponse.model_validate(
        service.create(payload.to_command())
    )


@router.get("/relations", response_model=list[KnowledgeRelationResponse])
def list_relations(
    service: RelationServiceDependency,
    source_item_id: Annotated[UUID, Query()],
) -> list[KnowledgeRelationResponse]:
    return [
        KnowledgeRelationResponse.model_validate(relation)
        for relation in service.list(source_item_id)
    ]

