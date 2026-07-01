"""Service health endpoint."""

from fastapi import APIRouter

from app.shared.responses import HealthResponse

router = APIRouter(tags=["System"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Report whether the API process is available."""
    return HealthResponse(status="ok", service="pia-api")

