"""Application version endpoint."""

from fastapi import APIRouter

from app.core.config import Settings, get_settings
from app.shared.responses import VersionResponse

router = APIRouter()


@router.get("/version", response_model=VersionResponse)
async def get_version() -> VersionResponse:
    """Return public build and environment information."""
    settings: Settings = get_settings()
    return VersionResponse(
        name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )
