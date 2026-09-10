"""Unit tests for sorting algorithms."""

import pytest

from algorithms.bubble_sort import bubble_sort
from algorithms.selection_sort import selection_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.merge_sort import merge_sort
from algorithms.quick_sort import quick_sort
from algorithms.heap_sort import heap_sort


ALGORITHMS = [
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    heap_sort,
]


@pytest.mark.parametrize("sort_fn", ALGORITHMS)
def test_sorts_correctly(sort_fn):
    input_array = [64, 34, 25, 12, 22, 11, 90]
    result = sort_fn(input_array)
    assert result["sorted_array"] == sorted(input_array)
    assert result["steps"][-1]["action"] == "done"


@pytest.mark.parametrize("sort_fn", ALGORITHMS)
def test_track_steps_disabled(sort_fn):
    result = sort_fn([5, 3, 8, 1], track_steps=False)
    assert result["sorted_array"] == [1, 3, 5, 8]
    assert result["steps"] == []


@pytest.mark.parametrize("sort_fn", ALGORITHMS)
def test_empty_array(sort_fn):
    result = sort_fn([])
    assert result["sorted_array"] == []


@pytest.mark.parametrize("sort_fn", ALGORITHMS)
def test_single_element(sort_fn):
    result = sort_fn([42])
    assert result["sorted_array"] == [42]


def test_result_structure():
    result = bubble_sort([3, 1, 2])
    assert {"algorithm", "sorted_array", "comparisons", "swaps", "steps"}.issubset(result.keys())
