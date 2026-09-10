"""Unit tests for array generator."""

import pytest

from utils.array_generator import generate_array, ARRAY_TYPES


def test_random_array_size():
    result = generate_array(25, "random", seed=42)
    assert len(result["array"]) == 25


def test_nearly_sorted_size_one():
    result = generate_array(1, "nearly_sorted")
    assert result["array"] == [1]


def test_few_unique_size_one():
    result = generate_array(1, "few_unique", seed=1)
    assert len(result["array"]) == 1


def test_invalid_size_raises():
    with pytest.raises(ValueError):
        generate_array(0, "random")


def test_max_size_enforced():
    with pytest.raises(ValueError):
        generate_array(1000, "random", max_size=150)
