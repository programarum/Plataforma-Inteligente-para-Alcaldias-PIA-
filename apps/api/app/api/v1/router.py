"""Router composition for API version 1."""

from fastapi import APIRouter

from app.api.v1.endpoints import health, version
from app.modules.departments.api.router import router as departments_router
from app.modules.municipalities.api.router import router as municipalities_router

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(version.router, tags=["version"])
api_router.include_router(municipalities_router, tags=["municipalities"])
api_router.include_router(departments_router, tags=["departments"])
