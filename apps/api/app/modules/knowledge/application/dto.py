"""Framework-independent Knowledge Core commands."""

from dataclasses import dataclass, field
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateKnowledgeItem:
    title: str
    summary: str
    source_type: str
    source_id: UUID
    municipality_id: UUID
    department_id: UUID | None = None
    tags: list[str] = field(default_factory=list)
    status: str = "active"


@dataclass(frozen=True, slots=True)
class UpdateKnowledgeItem:
    title: str | None = None
    summary: str | None = None
    tags: list[str] | None = None


@dataclass(frozen=True, slots=True)
class CreateKnowledgeRelation:
    source_item_id: UUID
    target_item_id: UUID
    relation_type: str
    description: str
    confidence_score: float

