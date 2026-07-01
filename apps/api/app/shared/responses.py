"""Shared response schemas exposed by foundational endpoints."""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health endpoint response schema."""

    status: Literal["ok"]
    service: str


class VersionResponse(BaseModel):
    """Version endpoint response schema."""

    name: str
    version: str
    environment: str
