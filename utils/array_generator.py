"""Array generation utilities for sorting benchmarks and visualizations."""

import random

ARRAY_TYPES = {
    "random": "Random Array",
    "sorted": "Sorted Array",
    "reverse": "Reverse Sorted Array",
    "nearly_sorted": "Nearly Sorted Array",
    "few_unique": "Few Unique Array",
}


def generate_array(size, array_type="random", seed=None, max_size=150):
    """
    Generate an array of the requested type and size.

    Raises:
        ValueError: If size or array_type is invalid.
    """
    if size < 1:
        raise ValueError("Array size must be at least 1.")
    if size > max_size:
        raise ValueError(f"Array size cannot exceed {max_size}.")
    if array_type not in ARRAY_TYPES:
        raise ValueError(
            f"Invalid array type '{array_type}'. "
            f"Valid types: {', '.join(ARRAY_TYPES.keys())}"
        )

    rng = random.Random(seed)

    if array_type == "random":
        arr = [rng.randint(1, max(size * 10, 10)) for _ in range(size)]
    elif array_type == "sorted":
        arr = list(range(1, size + 1))
    elif array_type == "reverse":
        arr = list(range(size, 0, -1))
    elif array_type == "nearly_sorted":
        arr = list(range(1, size + 1))
        if size >= 2:
            swaps = max(1, size // 10)
            for _ in range(swaps):
                i, j = rng.sample(range(size), 2)
                arr[i], arr[j] = arr[j], arr[i]
    elif array_type == "few_unique":
        unique_values = max(1, min(5, size))
        pool = [rng.randint(1, max(size * 2, 10)) for _ in range(unique_values)]
        arr = [rng.choice(pool) for _ in range(size)]

    return {"array_type": ARRAY_TYPES[array_type], "array": arr}
