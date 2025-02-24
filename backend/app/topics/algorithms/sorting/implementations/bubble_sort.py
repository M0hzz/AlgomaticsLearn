# backend/app/topics/algorithms/sorting/implementations/bubble_sort.py
from typing import List, Dict, Any

def bubble_sort(arr: List[int]) -> List[int]:
    """
    Implementation of bubble sort algorithm

    Args:
        arr: List of integers to sort

    Returns:
        Sorted list of integers
    """
    n = len(arr)
    result = arr.copy()

    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # Swap if the element found is greater than the next element
            if result[j] > result[j+1]:
                result[j], result[j+1] = result[j+1], result[j]

    return result

def get_bubble_sort_steps(arr: List[int]) -> List[Dict[str, Any]]:
    """
    Get step-by-step execution of bubble sort for visualization

    Args:
        arr: List of integers to sort

    Returns:
        List of dictionaries containing state at each step
    """
    steps = []
    n = len(arr)
    # Create a copy to avoid modifying the original
    array = arr.copy()

    # Add initial state
    steps.append({
        "array": array.copy(),
        "comparisons": [],
        "swaps": []
    })

    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # Add comparison step
            steps.append({
                "array": array.copy(),
                "comparisons": [j, j+1],
                "swaps": []
            })

            # Swap if the element found is greater than the next element
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]

                # Add swap step
                steps.append({
                    "array": array.copy(),
                    "comparisons": [],
                    "swaps": [j, j+1]
                })

    # Add final state
    steps.append({
        "array": array.copy(),
        "comparisons": [],
        "swaps": []
    })

    return steps

def get_algorithm_info() -> Dict[str, Any]:
    """
    Get information about bubble sort algorithm

    Returns:
        Dictionary with algorithm information
    """
    return {
        "name": "Bubble Sort",
        "category": "Sorting",
        "description": "A simple sorting algorithm that repeatedly steps through the list, "
                       "compares adjacent elements and swaps them if they are in the wrong order.",
        "time_complexity": {
            "best": "O(n)",
            "average": "O(n²)",
            "worst": "O(n²)"
        },
        "space_complexity": "O(1)",
        "stability": True
    }