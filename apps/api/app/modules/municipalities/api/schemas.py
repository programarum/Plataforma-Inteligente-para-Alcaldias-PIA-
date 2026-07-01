"""Pydantic schemas for the municipalities API."""

from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MunicipalityCreate(BaseModel):
    """Payload used to create a municipality."""

    name: str = Field(min_length=1, max_length=200)
    department: str = Field(min_length=1, max_length=120)
    country: str = Field(min_length=1, max_length=120)
    mayor_name: str = Field(min_length=1, max_length=200)
    government_period: str = Field(min_length=1, max_length=50)
    mission: str | None = None
    vision: str | None = None


class MunicipalityUpdate(BaseModel):
    """Payload used to partially update a municipality."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    department: str | None = Field(default=None, min_length=1, max_length=120)
    country: str | None = Field(default=None, min_length=1, max_length=120)
    mayor_name: str | None = Field(default=None, min_length=1, max_length=200)
    government_period: str | None = Field(default=None, min_length=1, max_length=50)
    mission: str | None = None
    vision: str | None = None

    @model_validator(mode="after")
    def prevent_null_required_fields(self) -> Self:
        """Reject explicit null values for required municipality fields."""
        required_fields = {
            "name",
            "department",
            "country",
            "mayor_name",
            "government_period",
        }
        null_fields = required_fields & self.model_fields_set
        if any(getattr(self, field_name) is None for field_name in null_fields):
            raise ValueError("Required municipality fields cannot be null")
        return self


class MunicipalityRead(BaseModel):
    """Public representation of a municipality."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    department: str
    country: str
    mayor_name: str
    government_period: str
    mission: str | None
    vision: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
