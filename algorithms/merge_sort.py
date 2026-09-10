"""Merge Sort — stable divide-and-conquer sorting."""

from algorithms.step_tracker import StepTracker
from config import Config


def merge_sort(array, track_steps=True):
    arr = array.copy()
    n = len(arr)
    tracker = StepTracker(track_steps=track_steps, max_steps=Config.MAX_ANIMATION_STEPS)
    tracker.start(arr)

    def merge(left, mid, right):
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]
        i = j = 0
        k = left

        while i < len(left_part) and j < len(right_part):
            left_idx = left + i
            right_idx = mid + 1 + j
            tracker.compare(arr, (left_idx, right_idx))
            if left_part[i] <= right_part[j]:
                if arr[k] != left_part[i]:
                    arr[k] = left_part[i]
                    tracker.write(arr, (k,), action="overwrite")
                i += 1
            else:
                if arr[k] != right_part[j]:
                    arr[k] = right_part[j]
                    tracker.write(arr, (k,), action="overwrite")
                j += 1
            k += 1

        while i < len(left_part):
            if arr[k] != left_part[i]:
                arr[k] = left_part[i]
                tracker.write(arr, (k,), action="overwrite")
            i += 1
            k += 1

        while j < len(right_part):
            if arr[k] != right_part[j]:
                arr[k] = right_part[j]
                tracker.write(arr, (k,), action="overwrite")
            j += 1
            k += 1

    def sort_range(left, right):
        if left < right:
            mid = (left + right) // 2
            sort_range(left, mid)
            sort_range(mid + 1, right)
            merge(left, mid, right)

    if n:
        sort_range(0, n - 1)

    tracker.finish(arr)
    return tracker.result("Merge Sort", arr)
