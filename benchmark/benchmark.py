"""Benchmark runner for comparing sorting algorithm performance."""

import statistics
import time

from config import Config
from registry.algorithm_registry import get_algorithm, get_algorithm_names


def _is_sorted(array):
    return all(array[i] <= array[i + 1] for i in range(len(array) - 1))


def run_single_sort(algorithm_name, array, include_steps=False):
    """
    Run one algorithm. Benchmark timing excludes step-recording overhead.
    """
    entry = get_algorithm(algorithm_name)
    sort_fn = entry["function"]

    if include_steps:
        start = time.perf_counter()
        result = sort_fn(array.copy(), track_steps=True)
        elapsed = time.perf_counter() - start
    else:
        sort_fn(array.copy(), track_steps=False)
        timings = []
        last_result = None
        for _ in range(Config.BENCHMARK_TIMED_RUNS):
            trial = array.copy()
            start = time.perf_counter()
            last_result = sort_fn(trial, track_steps=False)
            timings.append(time.perf_counter() - start)
        result = last_result
        elapsed = statistics.mean(timings)

    payload = {
        "algorithm": result["algorithm"],
        "execution_time": round(elapsed, 6),
        "comparisons": result["comparisons"],
        "swaps": result["swaps"],
        "sorted_array": result["sorted_array"],
        "verified": _is_sorted(result["sorted_array"]),
    }

    if include_steps:
        payload["steps"] = result["steps"]
        payload["steps_recorded"] = len(result["steps"])

    return payload


def run_benchmark(array, include_steps=False):
    results = [
        run_single_sort(name, array, include_steps=include_steps)
        for name in get_algorithm_names()
    ]
    return {"array_size": len(array), "results": results}


run_single_benchmark = run_single_sort
