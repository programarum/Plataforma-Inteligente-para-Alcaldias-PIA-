"""Application startup and shutdown lifecycle."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncIterator[None]:
    """Manage infrastructure resources owned by the API process."""
    yield
    engine.dispose()
