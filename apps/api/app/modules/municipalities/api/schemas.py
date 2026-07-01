"""Municipality HTTP request and response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.municipalities.application.dto import (
    CreateMunicipality,
    UpdateMunicipality,
)


class MunicipalityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    department: str = Field(min_length=1, max_length=200)
    country: str = Field(min_length=1, max_length=100)
    mayor_name: str = Field(min_length=1, max_length=200)
    government_period: str = Field(min_length=1, max_length=50)
    mission: str = Field(min_length=1)
    vision: str = Field(min_length=1)
    is_active: bool = True

    def to_command(self) -> CreateMunicipality:
        return CreateMunicipality(**self.model_dump())


class MunicipalityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    department: str | None = Field(default=None, min_length=1, max_length=200)
    country: str | None = Field(default=None, min_length=1, max_length=100)
    mayor_name: str | None = Field(default=None, min_length=1, max_length=200)
    government_period: str | None = Field(default=None, min_length=1, max_length=50)
    mission: str | None = Field(default=None, min_length=1)
    vision: str | None = Field(default=None, min_length=1)

    def to_command(self) -> UpdateMunicipality:
        return UpdateMunicipality(**self.model_dump())


class MunicipalityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    department: str
    country: str
    mayor_name: str
    government_period: str
    mission: str
    vision: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

