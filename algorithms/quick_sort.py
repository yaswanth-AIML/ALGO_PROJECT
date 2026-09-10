"""Quick Sort — partition-based sorting with median-of-three pivot."""

from algorithms.step_tracker import StepTracker
from config import Config


def _median_of_three(arr, low, high, tracker):
    mid = (low + high) // 2
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
        tracker.write(arr, (low, mid), action="swap")
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
        tracker.write(arr, (low, high), action="swap")
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
        tracker.write(arr, (mid, high), action="swap")
    arr[mid], arr[high] = arr[high], arr[mid]
    tracker.write(arr, (mid, high), action="swap")


def quick_sort(array, track_steps=True):
    arr = array.copy()
    tracker = StepTracker(track_steps=track_steps, max_steps=Config.MAX_ANIMATION_STEPS)
    tracker.start(arr)

    def partition(low, high):
        _median_of_three(arr, low, high, tracker)
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            tracker.compare(arr, (j, high))
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    tracker.write(arr, (i, j), action="swap")
        if i + 1 != high:
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            tracker.write(arr, (i + 1, high), action="swap")
        return i + 1

    def sort_range(low, high):
        if low < high:
            pivot_idx = partition(low, high)
            sort_range(low, pivot_idx - 1)
            sort_range(pivot_idx + 1, high)

    if arr:
        sort_range(0, len(arr) - 1)

    tracker.finish(arr)
    return tracker.result("Quick Sort", arr)
