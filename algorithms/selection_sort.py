"""Selection Sort — selects the minimum and swaps it into position."""

from algorithms.step_tracker import StepTracker
from config import Config


def selection_sort(array, track_steps=True):
    arr = array.copy()
    n = len(arr)
    tracker = StepTracker(track_steps=track_steps, max_steps=Config.MAX_ANIMATION_STEPS)
    tracker.start(arr)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            tracker.compare(arr, (min_idx, j))
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            tracker.write(arr, (i, min_idx), action="swap")

    tracker.finish(arr)
    return tracker.result("Selection Sort", arr)
