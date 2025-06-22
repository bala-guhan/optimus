import os
import json

def merge_sort(arr):
    """
    Sorts an array using the merge sort algorithm.

    Args:
        arr (list): The array to be sorted.

    Returns:
        list: The sorted array.
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    return merge(merge_sort(left_half), merge_sort(right_half))
    # No change needed

def merge(left, right):
    """
    Merges two sorted arrays into a single sorted array.

    Args:
        left (list): The first sorted array.
        right (list): The second sorted array.

    Returns:
        list: The merged sorted array.
    """
    merged = []
    left_index = 0
    right_index = 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    merged += left[left_index:]
    merged += right[right_index:]
    return merged



def merge(left, right):
    """
    Merges two sorted arrays into a single sorted array.

    Args:
        left (list): The first sorted array.
        right (list): The second sorted array.

    Returns:
        list: The merged sorted array.
    """
    merged = []
    left_index = 0
    right_index = 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    merged += left[left_index:]
    merged += right[right_index:]
    return merged



def quick_sort(arr: list):
    """
    Sorts an array using the quick sort algorithm.

    Args:
        arr (list): The array to be sorted.

    Returns:
        list: The sorted array.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)



l1 = [5,3,4,5,3,2,4,5,53.3,54,90,101]
print(quick_sort(l1))

