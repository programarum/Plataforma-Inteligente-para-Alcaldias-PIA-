"""Application version endpoint."""

from fastapi import APIRouter

from app.core.config import settings
from app.shared.responses import VersionResponse

router = APIRouter(tags=["System"])


@router.get("/version", response_model=VersionResponse)
async def version() -> VersionResponse:
    """Expose public build and environment information."""
    return VersionResponse(
        name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )

