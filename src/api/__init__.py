from fastapi import APIRouter

from api.documents import router as documents_router

router = APIRouter(prefix="/api")

router.include_router(documents_router)
