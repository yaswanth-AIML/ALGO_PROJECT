"""Central registry mapping algorithm metadata to sort functions."""

from algorithms.bubble_sort import bubble_sort
from algorithms.selection_sort import selection_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.merge_sort import merge_sort
from algorithms.quick_sort import quick_sort
from algorithms.heap_sort import heap_sort


ALGORITHM_REGISTRY = {
    "Bubble Sort": {
        "name": "Bubble Sort",
        "function": bubble_sort,
        "description": "Repeatedly compares adjacent elements and swaps them if out of order.",
        "best_case": "O(n)",
        "average_case": "O(n²)",
        "worst_case": "O(n²)",
        "space_complexity": "O(1)",
        "stable": True,
        "in_place": True,
    },
    "Selection Sort": {
        "name": "Selection Sort",
        "function": selection_sort,
        "description": "Finds the minimum element and places it at the front of the unsorted region.",
        "best_case": "O(n²)",
        "average_case": "O(n²)",
        "worst_case": "O(n²)",
        "space_complexity": "O(1)",
        "stable": False,
        "in_place": True,
    },
    "Insertion Sort": {
        "name": "Insertion Sort",
        "function": insertion_sort,
        "description": "Builds a sorted prefix by inserting each element into its correct position.",
        "best_case": "O(n)",
        "average_case": "O(n²)",
        "worst_case": "O(n²)",
        "space_complexity": "O(1)",
        "stable": True,
        "in_place": True,
    },
    "Merge Sort": {
        "name": "Merge Sort",
        "function": merge_sort,
        "description": "Recursively divides the array and merges sorted halves.",
        "best_case": "O(n log n)",
        "average_case": "O(n log n)",
        "worst_case": "O(n log n)",
        "space_complexity": "O(n)",
        "stable": True,
        "in_place": False,
    },
    "Quick Sort": {
        "name": "Quick Sort",
        "function": quick_sort,
        "description": "Partitions around a pivot using median-of-three selection.",
        "best_case": "O(n log n)",
        "average_case": "O(n log n)",
        "worst_case": "O(n²)",
        "space_complexity": "O(log n)",
        "stable": False,
        "in_place": True,
    },
    "Heap Sort": {
        "name": "Heap Sort",
        "function": heap_sort,
        "description": "Builds a max-heap and repeatedly extracts the largest element.",
        "best_case": "O(n log n)",
        "average_case": "O(n log n)",
        "worst_case": "O(n log n)",
        "space_complexity": "O(1)",
        "stable": False,
        "in_place": True,
    },
}


def get_algorithm(name):
    if name not in ALGORITHM_REGISTRY:
        raise KeyError(f"Algorithm '{name}' is not registered.")
    return ALGORITHM_REGISTRY[name]


def get_all_algorithms():
    return ALGORITHM_REGISTRY


def get_algorithm_names():
    return list(ALGORITHM_REGISTRY.keys())
