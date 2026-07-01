"""Router composition for API version 1."""

from fastapi import APIRouter

from app.api.v1.endpoints import health, version

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(version.router, tags=["version"])
