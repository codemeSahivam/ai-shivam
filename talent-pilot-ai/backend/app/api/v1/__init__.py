from fastapi import APIRouter

from app.api.v1.analyze import router as analyze_router
from app.api.v1.auth import router as auth_router
from app.api.v1.history import router as history_router
from app.api.v1.samples import router as samples_router

api_router = APIRouter()
api_router.include_router(analyze_router)
api_router.include_router(auth_router)
api_router.include_router(history_router)
api_router.include_router(samples_router)
