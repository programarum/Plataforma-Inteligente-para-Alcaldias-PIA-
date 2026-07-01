"""Document HTTP schemas."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.documents.application.dto import (
    CreateDocument,
    CreateDocumentChunk,
    UpdateDocument,
)


class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1)
    document_type: str = Field(min_length=1, max_length=100)
    source: str = Field(min_length=1, max_length=200)
    file_path: str = Field(min_length=1, max_length=1000)
    file_name: str = Field(min_length=1, max_length=300)
    file_extension: str = Field(min_length=1, max_length=20)
    mime_type: str = Field(min_length=1, max_length=150)
    size_bytes: int = Field(ge=0)
    checksum: str = Field(min_length=1, max_length=128)
    version: str = Field(min_length=1, max_length=50)
    status: Literal["active", "archived"] = "active"
    confidentiality_level: str = Field(min_length=1, max_length=30)
    municipality_id: UUID
    department_id: UUID
    uploaded_by_id: UUID | None = None

    def to_command(self) -> CreateDocument:
        return CreateDocument(**self.model_dump())


class DocumentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = Field(default=None, min_length=1)
    document_type: str | None = Field(default=None, min_length=1, max_length=100)
    source: str | None = Field(default=None, min_length=1, max_length=200)
    file_path: str | None = Field(default=None, min_length=1, max_length=1000)
    file_name: str | None = Field(default=None, min_length=1, max_length=300)
    file_extension: str | None = Field(default=None, min_length=1, max_length=20)
    mime_type: str | None = Field(default=None, min_length=1, max_length=150)
    size_bytes: int | None = Field(default=None, ge=0)
    checksum: str | None = Field(default=None, min_length=1, max_length=128)
    version: str | None = Field(default=None, min_length=1, max_length=50)
    confidentiality_level: str | None = Field(
        default=None, min_length=1, max_length=30
    )

    def to_command(self) -> UpdateDocument:
        return UpdateDocument(**self.model_dump())


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    document_type: str
    source: str
    file_path: str
    file_name: str
    file_extension: str
    mime_type: str
    size_bytes: int
    checksum: str
    version: str
    status: str
    confidentiality_level: str
    municipality_id: UUID
    department_id: UUID
    uploaded_by_id: UUID | None
    created_at: datetime
    updated_at: datetime


class DocumentChunkCreate(BaseModel):
    chunk_index: int = Field(ge=0)
    content: str = Field(min_length=1)
    page_number: int | None = Field(default=None, ge=1)
    metadata: dict[str, object] = Field(default_factory=dict)

    def to_command(self) -> CreateDocumentChunk:
        return CreateDocumentChunk(**self.model_dump())


class DocumentChunkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    document_id: UUID
    chunk_index: int
    content: str
    page_number: int | None
    metadata: dict[str, object] = Field(validation_alias="metadata_")
    created_at: datetime

