"""Shared response contracts."""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health endpoint response."""

    status: Literal["ok"]
    service: str


class VersionResponse(BaseModel):
    """Version endpoint response."""

    name: str
    version: str
    environment: str

