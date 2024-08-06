# coding: utf-8
import pytest
from .solution import count_combinations


@pytest.mark.parametrize('springs, groups, expected', [
    ('???.###', [1, 1, 3], 1),
    ('.??..??...?##.', [1, 1, 3], 4),
    ('?#?#?#?#?#?#?#?', [1, 3, 1, 6], 1),
    ('????.#...#...', [4, 1, 1], 1),
    ('????.######..#####.', [1, 6, 5], 4),
    ('?###????????', [3, 2, 1], 10),
])
def test_count_combinations(springs, groups, expected):
    assert count_combinations(springs, groups) == expected
