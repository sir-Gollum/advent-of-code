# coding: utf-8
import pytest
from .solution import fully_contains, overlaps


@pytest.mark.parametrize(
    'range1, range2, expected',
    [
        ((2, 4), (6, 8), False),
        ((2, 3), (4, 5), False),
        ((5, 7), (7, 9), False),
        ((2, 8), (3, 7), True),
        ((6, 6), (4, 6), True),
        ((2, 6), (4, 8), False),
    ]
)
def test_fully_contains(range1, range2, expected):
    assert fully_contains(range1, range2) == expected
    assert fully_contains(range2, range1) == expected


@pytest.mark.parametrize(
    'range1, range2, expected',
    [
        ((2, 4), (6, 8), False),
        ((2, 3), (4, 5), False),
        ((5, 7), (7, 9), True),
        ((2, 8), (3, 7), True),
        ((6, 6), (4, 6), True),
        ((2, 6), (4, 8), True),
    ]
)
def test_overlaps(range1, range2, expected):
    assert overlaps(range1, range2) == expected
    assert overlaps(range2, range1) == expected
