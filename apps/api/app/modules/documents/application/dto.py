"""Framework-independent document commands."""

from dataclasses import dataclass, field
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateDocument:
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
    confidentiality_level: str
    municipality_id: UUID
    department_id: UUID
    uploaded_by_id: UUID | None = None
    status: str = "active"


@dataclass(frozen=True, slots=True)
class UpdateDocument:
    title: str | None = None
    description: str | None = None
    document_type: str | None = None
    source: str | None = None
    file_path: str | None = None
    file_name: str | None = None
    file_extension: str | None = None
    mime_type: str | None = None
    size_bytes: int | None = None
    checksum: str | None = None
    version: str | None = None
    confidentiality_level: str | None = None


@dataclass(frozen=True, slots=True)
class CreateDocumentChunk:
    chunk_index: int
    content: str
    page_number: int | None = None
    metadata: dict[str, object] = field(default_factory=dict)

