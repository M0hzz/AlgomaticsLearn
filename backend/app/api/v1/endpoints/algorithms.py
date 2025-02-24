# backend/app/api/v1/endpoints/algorithms.py
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from backend.app.topics.algorithms.sorting.implementations.bubble_sort import (
    bubble_sort, get_bubble_sort_steps, get_algorithm_info
)

router = APIRouter()

@router.post("/sorting/bubble-sort")
async def run_bubble_sort(data: List[int]) -> List[int]:
    """
    Run bubble sort algorithm on input data
    """
    try:
        return bubble_sort(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sorting/bubble-sort/steps")
async def get_bubble_sort_visualization(data: List[int]) -> List[Dict[str, Any]]:
    """
    Get step-by-step visualization data for bubble sort
    """
    try:
        return get_bubble_sort_steps(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sorting/bubble-sort/info")
async def get_bubble_sort_info() -> Dict[str, Any]:
    """
    Get information about bubble sort algorithm
    """
    return get_algorithm_info()