"""FastAPI application entry point."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.logging import configure_logging
from app.shared.exceptions import NotFoundError


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

    @application.exception_handler(NotFoundError)
    async def not_found_handler(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": exc.detail})

    return application


app = create_app()
