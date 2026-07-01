"""Knowledge item and relation use cases."""

from dataclasses import asdict
from uuid import UUID

from app.modules.departments.domain.repositories import DepartmentRepository
from app.modules.documents.domain.repositories import DocumentRepository
from app.modules.knowledge.application.dto import (
    CreateKnowledgeItem,
    CreateKnowledgeRelation,
    UpdateKnowledgeItem,
)
from app.modules.knowledge.domain.models import KnowledgeItem, KnowledgeRelation
from app.modules.knowledge.domain.repositories import (
    KnowledgeItemRepository,
    KnowledgeRelationRepository,
)
from app.modules.municipalities.domain.repositories import MunicipalityRepository
from app.shared.exceptions import NotFoundError


class KnowledgeItemService:
    def __init__(
        self,
        repository: KnowledgeItemRepository,
        municipalities: MunicipalityRepository,
        departments: DepartmentRepository,
        documents: DocumentRepository,
    ) -> None:
        self._repository = repository
        self._municipalities = municipalities
        self._departments = departments
        self._documents = documents

    def create(self, command: CreateKnowledgeItem) -> KnowledgeItem:
        if self._municipalities.get(command.municipality_id) is None:
            raise NotFoundError("Municipality not found")
        if command.department_id is not None:
            department = self._departments.get(command.department_id)
            if (
                department is None
                or department.municipality_id != command.municipality_id
            ):
                raise NotFoundError("Department not found for municipality")
        if (
            command.source_type == "document"
            and self._documents.get(command.source_id) is None
        ):
            raise NotFoundError("Source document not found")
        return self._repository.add(KnowledgeItem(**asdict(command)))

    def list(self) -> list[KnowledgeItem]:
        return self._repository.list()

    def get(self, item_id: UUID) -> KnowledgeItem:
        item = self._repository.get(item_id)
        if item is None:
            raise NotFoundError("Knowledge item not found")
        return item

    def update(self, item_id: UUID, command: UpdateKnowledgeItem) -> KnowledgeItem:
        item = self.get(item_id)
        for name, value in asdict(command).items():
            if value is not None:
                setattr(item, name, value)
        return self._repository.save(item)

    def archive(self, item_id: UUID) -> KnowledgeItem:
        item = self.get(item_id)
        item.status = "archived"
        return self._repository.save(item)


class KnowledgeRelationService:
    def __init__(
        self,
        repository: KnowledgeRelationRepository,
        items: KnowledgeItemRepository,
    ) -> None:
        self._repository = repository
        self._items = items

    def create(self, command: CreateKnowledgeRelation) -> KnowledgeRelation:
        if self._items.get(command.source_item_id) is None:
            raise NotFoundError("Source knowledge item not found")
        if self._items.get(command.target_item_id) is None:
            raise NotFoundError("Target knowledge item not found")
        return self._repository.add(KnowledgeRelation(**asdict(command)))

    def list(self, source_item_id: UUID) -> list[KnowledgeRelation]:
        if self._items.get(source_item_id) is None:
            raise NotFoundError("Source knowledge item not found")
        return self._repository.list_by_source(source_item_id)
