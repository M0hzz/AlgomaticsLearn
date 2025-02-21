from fastapi import APIRouter
from api.auth import router as auth_router

router = APIRouter()

# Include authentication routes
router.include_router(auth_router, prefix="/auth")
