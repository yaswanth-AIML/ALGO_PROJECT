"""Request payload validation."""

from config import Config


def validate_array_size(size):
    """Coerce and validate array size."""
    try:
        size = int(size)
    except (TypeError, ValueError) as exc:
        raise ValueError("Array size must be a valid integer.") from exc

    if size < Config.MIN_ARRAY_SIZE:
        raise ValueError(f"Array size must be at least {Config.MIN_ARRAY_SIZE}.")
    if size > Config.MAX_ARRAY_SIZE:
        raise ValueError(f"Array size cannot exceed {Config.MAX_ARRAY_SIZE}.")
    return size


def validate_sort_array(array):
    """Validate client-provided array for sort/benchmark endpoints."""
    if not isinstance(array, list):
        raise ValueError("Array must be a JSON list of numbers.")
    if not array:
        raise ValueError("A non-empty array is required.")
    if len(array) > Config.MAX_ARRAY_SIZE:
        raise ValueError(f"Array cannot exceed {Config.MAX_ARRAY_SIZE} elements.")

    validated = []
    for index, value in enumerate(array):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"Element at index {index} must be a number.")
        validated.append(int(value) if float(value).is_integer() else float(value))
    return validated


def validate_array_type(array_type, valid_types):
    """Validate array type key."""
    if array_type not in valid_types:
        raise ValueError(
            f"Invalid array type '{array_type}'. "
            f"Valid types: {', '.join(valid_types.keys())}"
        )
    return array_type
