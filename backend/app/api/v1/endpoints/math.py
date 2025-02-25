# backend/app/api/v1/endpoints/math.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def read_math_data():
    return {"message": "Math endpoint"}