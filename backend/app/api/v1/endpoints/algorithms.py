# backend/app/api/v1/endpoints/algorithms.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from backend.app.core.security import get_current_user
from backend.app.models.user import User

from backend.app.topics.algorithms.sorting.bubble_sort import (
    bubble_sort, get_bubble_sort_steps, get_algorithm_info as get_bubble_sort_info
)
from backend.app.topics.algorithms.sorting.quick_sort import (
    quick_sort, get_quick_sort_steps, get_algorithm_info as get_quick_sort_info
)

router = APIRouter()

# Sorting algorithms
@router.post("/sorting/bubble-sort")
async def run_bubble_sort(data: List[int], current_user: User = Depends(get_current_user)):
    """Run bubble sort algorithm"""
    try:
        return {"sorted_array": bubble_sort(data)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sorting/bubble-sort/steps")
async def get_bubble_sort_visualization(data: List[int], current_user: User = Depends(get_current_user)):
    """Get visualization steps for bubble sort"""
    try:
        return {"steps": get_bubble_sort_steps(data)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sorting/bubble-sort/info")
async def get_bubble_sort_information():
    """Get information about bubble sort algorithm"""
    return get_bubble_sort_info()

@router.post("/sorting/quick-sort")
async def run_quick_sort(data: List[int], current_user: User = Depends(get_current_user)):
    """Run quick sort algorithm"""
    try:
        return {"sorted_array": quick_sort(data)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sorting/quick-sort/steps")
async def get_quick_sort_visualization(data: List[int], current_user: User = Depends(get_current_user)):
    """Get visualization steps for quick sort"""
    try:
        return {"steps": get_quick_sort_steps(data)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sorting/quick-sort/info")
async def get_quick_sort_information():
    """Get information about quick sort algorithm"""
    return get_quick_sort_info()

# Execute user code
@router.post("/execute")
async def execute_algorithm(code: str, data: List[int], current_user: User = Depends(get_current_user)):
    """Execute user algorithm code with provided data"""
    try:
        # Warning: This is a simplified version. In a real app, you would need
        # to implement proper sandboxing to execute user code safely.
        # For now, we just return an error
        raise HTTPException(
            status_code=501,
            detail="Code execution is not implemented for security reasons"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Compare algorithms
@router.post("/compare")
async def compare_algorithms(
        data: List[int],
        algorithms: List[str] = ["bubble_sort", "quick_sort"],
        current_user: User = Depends(get_current_user)
):
    """Compare different sorting algorithms"""
    import time

    try:
        results = {}
        available_algorithms = {
            "bubble_sort": bubble_sort,
            "quick_sort": quick_sort
        }

        for algo_name in algorithms:
            if algo_name not in available_algorithms:
                raise HTTPException(
                    status_code=400,
                    detail=f"Algorithm '{algo_name}' not found"
                )

            algo_func = available_algorithms[algo_name]

            # Measure execution time
            start_time = time.time()
            sorted_array = algo_func(data)
            end_time = time.time()

            results[algo_name] = {
                "execution_time_ms": round((end_time - start_time) * 1000, 2),
                "sorted_array": sorted_array
            }

        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))