# backend/app/topics/algorithms/sorting/quick_sort.py
from typing import List, Dict, Any

def quick_sort(arr: List[int]) -> List[int]:
    """
    Implementation of quick sort algorithm

    Args:
        arr: List of integers to sort

    Returns:
        Sorted list of integers
    """
    # Create a copy to avoid modifying the original
    result = arr.copy()

    def _quick_sort(arr, low, high):
        if low < high:
            # Partition the array and get the pivot index
            pivot_idx = _partition(arr, low, high)

            # Sort the left part
            _quick_sort(arr, low, pivot_idx - 1)

            # Sort the right part
            _quick_sort(arr, pivot_idx + 1, high)

    def _partition(arr, low, high):
        # Choose the rightmost element as pivot
        pivot = arr[high]

        # Index of smaller element
        i = low - 1

        for j in range(low, high):
            # If current element is smaller than or equal to pivot
            if arr[j] <= pivot:
                # Increment index of smaller element
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        # Place pivot at its correct position
        arr[i + 1], arr[high] = arr[high], arr[i + 1]

        # Return the position where partition is done
        return i + 1

    if len(result) > 1:
        _quick_sort(result, 0, len(result) - 1)

    return result

def get_quick_sort_steps(arr: List[int]) -> List[Dict[str, Any]]:
    """
    Get step-by-step execution of quick sort for visualization

    Args:
        arr: List of integers to sort

    Returns:
        List of dictionaries containing state at each step
    """
    steps = []
    # Create a copy to avoid modifying the original
    array = arr.copy()

    # Add initial state
    steps.append({
        "array": array.copy(),
        "pivot": None,
        "left": None,
        "right": None,
        "swaps": []
    })

    def _quick_sort(arr, low, high, depth=0):
        if low < high:
            # Add partitioning step
            steps.append({
                "array": arr.copy(),
                "partition": [low, high],
                "depth": depth
            })

            # Partition the array and get the pivot index
            pivot_idx = _partition(arr, low, high, depth)

            # Sort the left part
            _quick_sort(arr, low, pivot_idx - 1, depth + 1)

            # Sort the right part
            _quick_sort(arr, pivot_idx + 1, high, depth + 1)

    def _partition(arr, low, high, depth):
        # Choose the rightmost element as pivot
        pivot = arr[high]

        # Add pivot selection step
        steps.append({
            "array": arr.copy(),
            "pivot_idx": high,
            "pivot_value": pivot,
            "range": [low, high],
            "depth": depth
        })

        # Index of smaller element
        i = low - 1

        for j in range(low, high):
            # Add comparison step
            steps.append({
                "array": arr.copy(),
                "pivot_idx": high,
                "comparing": j,
                "i": i,
                "depth": depth
            })

            # If current element is smaller than or equal to pivot
            if arr[j] <= pivot:
                # Increment index of smaller element
                i += 1

                # Swap if needed
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]

                    # Add swap step
                    steps.append({
                        "array": arr.copy(),
                        "swaps": [i, j],
                        "pivot_idx": high,
                        "depth": depth
                    })

        # Place pivot at its correct position
        if i + 1 != high:
            arr[i + 1], arr[high] = arr[high], arr[i + 1]

            # Add pivot placement step
            steps.append({
                "array": arr.copy(),
                "swaps": [i + 1, high],
                "pivot_placement": True,
                "depth": depth
            })

        # Return the position where partition is done
        return i + 1

    if len(array) > 1:
        _quick_sort(array, 0, len(array) - 1)

    # Add final state
    steps.append({
        "array": array.copy(),
        "pivot": None,
        "left": None,
        "right": None,
        "swaps": [],
        "final": True
    })

    return steps

def get_algorithm_info() -> Dict[str, Any]:
    """
    Get information about quick sort algorithm

    Returns:
        Dictionary with algorithm information
    """
    return {
        "name": "Quick Sort",
        "category": "Sorting",
        "description": "Quick sort is a divide-and-conquer algorithm that picks an element as a pivot "
                       "and partitions the array around the pivot. The key process is the partition() "
                       "function which places the pivot at its correct position.",
        "time_complexity": {
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n²)"
        },
        "space_complexity": "O(log n)",
        "stability": False
    }