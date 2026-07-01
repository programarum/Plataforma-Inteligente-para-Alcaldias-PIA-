"""Pydantic schemas for the departments API."""

from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DepartmentCreate(BaseModel):
    """Payload used to create a municipal department."""

    municipality_id: UUID
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    manager_name: str | None = Field(default=None, max_length=200)


class DepartmentUpdate(BaseModel):
    """Payload used to partially update a municipal department."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    manager_name: str | None = Field(default=None, max_length=200)

    @model_validator(mode="after")
    def prevent_null_name(self) -> Self:
        """Reject an explicit null value for the required name field."""
        if "name" in self.model_fields_set and self.name is None:
            raise ValueError("Department name cannot be null")
        return self


class DepartmentRead(BaseModel):
    """Public representation of a municipal department."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    municipality_id: UUID
    name: str
    description: str | None
    manager_name: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
