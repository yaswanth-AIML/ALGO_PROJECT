"""Complexity metadata helpers."""

from registry.algorithm_registry import get_algorithm


def format_complexity_panel(algorithm_name):
    entry = get_algorithm(algorithm_name)
    return {
        "algorithm": entry["name"],
        "description": entry.get("description", ""),
        "best_case": entry["best_case"],
        "average_case": entry["average_case"],
        "worst_case": entry["worst_case"],
        "space_complexity": entry["space_complexity"],
        "stable": entry["stable"],
        "in_place": entry["in_place"],
    }
