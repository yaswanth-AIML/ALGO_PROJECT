"""Shared step tracking for sorting visualizations."""


class StepTracker:
    """
    Tracks comparisons, writes, and thinned animation steps.

    When steps exceed max_steps, intermediate frames are sampled so payloads
    stay performant while metrics remain exact.
    """

    __slots__ = ("steps", "comparisons", "writes", "track_steps", "max_steps", "_interval", "_ops")

    def __init__(self, track_steps=True, max_steps=2500):
        self.steps = []
        self.comparisons = 0
        self.writes = 0
        self.track_steps = track_steps
        self.max_steps = max_steps
        self._interval = 1
        self._ops = 0

    def record(self, arr, compared=None, swapped=None, action="compare", force=False):
        if not self.track_steps:
            return

        if force or action in ("start", "done"):
            self.steps.append(self._frame(arr, compared, swapped, action))
            return

        self._ops += 1
        if len(self.steps) >= self.max_steps - 2:
            self._interval = max(self._interval, self._ops // max(self.max_steps, 1) + 1)

        if self._ops % self._interval == 0:
            self.steps.append(self._frame(arr, compared, swapped, action))

    def compare(self, arr, indices, action="compare"):
        self.comparisons += 1
        self.record(arr, compared=list(indices), action=action)

    def write(self, arr, indices, action="swap"):
        self.writes += 1
        self.record(arr, swapped=list(indices), action=action)

    def start(self, arr):
        self.record(arr, action="start", force=True)

    def finish(self, arr):
        self.record(arr, action="done", force=True)

    def result(self, algorithm_name, sorted_array):
        return {
            "algorithm": algorithm_name,
            "sorted_array": sorted_array,
            "comparisons": self.comparisons,
            "swaps": self.writes,
            "steps": self.steps,
        }

    @staticmethod
    def _frame(arr, compared, swapped, action):
        return {
            "array": arr.copy(),
            "compared": compared or [],
            "swapped": swapped or [],
            "action": action,
        }
