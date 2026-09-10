"""Insertion Sort — builds the sorted region one element at a time."""

from algorithms.step_tracker import StepTracker
from config import Config


def insertion_sort(array, track_steps=True):
    arr = array.copy()
    n = len(arr)
    tracker = StepTracker(track_steps=track_steps, max_steps=Config.MAX_ANIMATION_STEPS)
    tracker.start(arr)

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0:
            tracker.compare(arr, (j, j + 1))
            if arr[j] > key:
                arr[j + 1] = arr[j]
                tracker.write(arr, (j, j + 1), action="overwrite")
                j -= 1
            else:
                break
        if j + 1 != i:
            arr[j + 1] = key
            tracker.write(arr, (j + 1,), action="overwrite")

    tracker.finish(arr)
    return tracker.result("Insertion Sort", arr)
