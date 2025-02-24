# backend/app/api/v1/api.py
from fastapi import APIRouter

from backend.app.api.v1.endpoints import auth, test, wix, algorithms, math

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(test.router, prefix="/test", tags=["test"])
api_router.include_router(wix.router, prefix="/wix", tags=["wix"])
api_router.include_router(algorithms.router, prefix="/algorithms", tags=["algorithms"])
api_router.include_router(math.router, prefix="/math", tags=["math"])