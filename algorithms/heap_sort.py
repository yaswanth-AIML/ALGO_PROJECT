"""Heap Sort — in-place heap-based sorting."""

from algorithms.step_tracker import StepTracker
from config import Config


def heap_sort(array, track_steps=True):
    arr = array.copy()
    n = len(arr)
    tracker = StepTracker(track_steps=track_steps, max_steps=Config.MAX_ANIMATION_STEPS)
    tracker.start(arr)

    def heapify(size, root):
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < size:
            tracker.compare(arr, (largest, left))
            if arr[left] > arr[largest]:
                largest = left
        if right < size:
            tracker.compare(arr, (largest, right))
            if arr[right] > arr[largest]:
                largest = right
        if largest != root:
            arr[root], arr[largest] = arr[largest], arr[root]
            tracker.write(arr, (root, largest), action="swap")
            heapify(size, largest)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        tracker.write(arr, (0, i), action="swap")
        heapify(i, 0)

    tracker.finish(arr)
    return tracker.result("Heap Sort", arr)
