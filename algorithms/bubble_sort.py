"""Bubble Sort — repeatedly swaps adjacent out-of-order elements."""

from algorithms.step_tracker import StepTracker
from config import Config


def bubble_sort(array, track_steps=True):
    arr = array.copy()
    n = len(arr)
    tracker = StepTracker(track_steps=track_steps, max_steps=Config.MAX_ANIMATION_STEPS)
    tracker.start(arr)

    for i in range(n):
        swapped_flag = False
        for j in range(n - i - 1):
            tracker.compare(arr, (j, j + 1))
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped_flag = True
                tracker.write(arr, (j, j + 1), action="swap")
        if not swapped_flag:
            break

    tracker.finish(arr)
    return tracker.result("Bubble Sort", arr)
