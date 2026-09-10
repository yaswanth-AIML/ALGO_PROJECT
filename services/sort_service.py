"""Sorting and benchmark orchestration."""

from config import Config
from benchmark.benchmark import run_benchmark, run_single_sort
from benchmark.complexity import format_complexity_panel
from registry.algorithm_registry import get_algorithm, get_algorithm_names
from utils.array_generator import ARRAY_TYPES, generate_array


def list_catalog():
    """Return algorithms, array types, and API limits."""
    algorithms = []
    for name in get_algorithm_names():
        entry = get_algorithm(name)
        algorithms.append({
            "name": entry["name"],
            "description": entry.get("description", ""),
            "best_case": entry["best_case"],
            "average_case": entry["average_case"],
            "worst_case": entry["worst_case"],
            "space_complexity": entry["space_complexity"],
            "stable": entry["stable"],
            "in_place": entry["in_place"],
        })

    return {
        "algorithms": algorithms,
        "array_types": [{"key": key, "label": label} for key, label in ARRAY_TYPES.items()],
        "limits": {
            "min_array_size": Config.MIN_ARRAY_SIZE,
            "max_array_size": Config.MAX_ARRAY_SIZE,
            "max_animation_steps": Config.MAX_ANIMATION_STEPS,
        },
    }


def generate(size, array_type, seed=None):
    return generate_array(size, array_type, seed=seed, max_size=Config.MAX_ARRAY_SIZE)


def sort(algorithm_name, array):
    result = run_single_sort(algorithm_name, array, include_steps=True)
    return {
        "result": result,
        "complexity": format_complexity_panel(algorithm_name),
    }


def benchmark(array):
    return run_benchmark(array, include_steps=False)
