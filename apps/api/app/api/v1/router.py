"""API v1 router composition."""

from fastapi import APIRouter

from app.api.v1.endpoints import health, version
from app.modules.departments.api.router import router as departments_router
from app.modules.documents.api.router import router as documents_router
from app.modules.knowledge.api.router import router as knowledge_router
from app.modules.municipalities.api.router import router as municipalities_router

router = APIRouter()
router.include_router(health.router)
router.include_router(version.router)
router.include_router(municipalities_router)
router.include_router(departments_router)
router.include_router(documents_router)
router.include_router(knowledge_router)
