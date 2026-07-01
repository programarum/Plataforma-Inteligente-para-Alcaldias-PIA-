"""Service health endpoint."""

from fastapi import APIRouter

from app.shared.responses import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    """Return the operational status of the API process."""
    return HealthResponse(status="ok", service="pia-api")
