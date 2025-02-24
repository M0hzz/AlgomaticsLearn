# backend/app/api/v1/api.py
from fastapi import APIRouter

from ..v1.endpoints import auth, algorithms

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(algorithms.router, prefix="/algorithms", tags=["algorithms"])
