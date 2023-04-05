# coding: utf-8
import pytest
from collections import deque
from .solution import move



@pytest.mark.parametrize(
    'items, positions, idx_to_mode, expected_items, expected_positions',
    [
        (
            [1, 2, -3, 3, -2, 0, 4],
            [0, 1, 2, 3, 4, 5, 6],
            0,
            [2, 1, -3, 3, -2, 0, 4],
            [1, 0, 2, 3, 4, 5, 6],
        ),
        (
            [2, 1, -3, 3, -2, 0, 4],
            [1, 0, 2, 3, 4, 5, 6],
            1,
            [1, -3, 2, 3, -2, 0, 4],
            [0, 2, 1, 3, 4, 5, 6],
        ),
        (
            [1, -3, 2, 3, -2, 0, 4],
            [0, 2, 1, 3, 4, 5, 6],
            2,
            [1, 2, 3, -2, -3, 0, 4],
            [0, 1, 3, 4, 2, 5, 6],
        ),
    ]
)
def test_move(items, positions, idx_to_mode, expected_items, expected_positions):
    items = deque(items)
    positions = deque(positions)
    move(items, positions, idx_to_mode)
    assert list(items) == expected_items
    assert list(positions) == expected_positions


