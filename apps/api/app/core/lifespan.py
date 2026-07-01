"""Application startup and shutdown lifecycle."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Manage application-level infrastructure resources."""
    logger.info("PIA API started")
    yield
    engine.dispose()
    logger.info("PIA API stopped")

