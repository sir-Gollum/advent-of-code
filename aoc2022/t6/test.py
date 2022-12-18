# coding: utf-8
import pytest
from .solution import find_start_marker_idx


@pytest.mark.parametrize(
    'stream, expected',
    [
        ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7),
        ('bvwbjplbgvbhsrlpgdmjqwftvncz', 5),
        ('nppdvjthqldpwncqszvftbrmjlhg', 6),
        ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10),
        ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11),
    ]
)
def test_find_start_marker_idx_packet(stream, expected):
    assert find_start_marker_idx(stream, 4) == expected


@pytest.mark.parametrize(
    'stream, expected',
    [
        ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 19),
        ('bvwbjplbgvbhsrlpgdmjqwftvncz', 23),
        ('nppdvjthqldpwncqszvftbrmjlhg', 23),
        ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 29),
        ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 26),
    ]
)
def test_find_start_marker_idx_message(stream, expected):
    assert find_start_marker_idx(stream, 14) == expected
