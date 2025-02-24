#Quick sort

def quick_sort(arr):
    """Quick Sort Algo (Recursive)"""
    if len(arr) <= 1:
        return arr # Base case: if array have 1 or 0 elements, array is sorted

    pivot = arr[len(arr) // 2] # chose middle element as pivot
    left = [x for x in arr if x < pivot] # elements < pivot
    middle = [x for x in arr if x == pivot] # elements = pivot
    right =  [x for x in arr if x > pivot] # elements > pivot

    return quick_sort(left) + middle + quick_sort(right)


# run
arr = [10, 7, 8, 9, 1, 5]
sorted_arr = quick_sort(arr)
print("Sorted Array:", sorted_arr)  # Output [1, 5, 7, 8, 9, 10]