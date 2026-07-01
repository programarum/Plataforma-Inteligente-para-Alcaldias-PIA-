"""Knowledge Core HTTP schemas."""

from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.modules.knowledge.application.dto import (
    CreateKnowledgeItem,
    CreateKnowledgeRelation,
    UpdateKnowledgeItem,
)


class KnowledgeItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    summary: str = Field(min_length=1)
    source_type: str = Field(min_length=1, max_length=50)
    source_id: UUID
    municipality_id: UUID
    department_id: UUID | None = None
    tags: list[str] = Field(default_factory=list)
    status: str = Field(default="active", min_length=1, max_length=30)

    def to_command(self) -> CreateKnowledgeItem:
        return CreateKnowledgeItem(**self.model_dump())


class KnowledgeItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    summary: str | None = Field(default=None, min_length=1)
    tags: list[str] | None = None

    def to_command(self) -> UpdateKnowledgeItem:
        return UpdateKnowledgeItem(**self.model_dump())


class KnowledgeItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    summary: str
    source_type: str
    source_id: UUID
    municipality_id: UUID
    department_id: UUID | None
    tags: list[str]
    status: str
    created_at: datetime
    updated_at: datetime


class KnowledgeRelationCreate(BaseModel):
    source_item_id: UUID
    target_item_id: UUID
    relation_type: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    confidence_score: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def distinct_items(self) -> Self:
        if self.source_item_id == self.target_item_id:
            raise ValueError("Knowledge relation items must be different")
        return self

    def to_command(self) -> CreateKnowledgeRelation:
        return CreateKnowledgeRelation(**self.model_dump())


class KnowledgeRelationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_item_id: UUID
    target_item_id: UUID
    relation_type: str
    description: str
    confidence_score: float
    created_at: datetime

