"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    configure_logging()
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )
    application.include_router(api_v1_router, prefix="/api/v1")
    return application


app = create_app()

