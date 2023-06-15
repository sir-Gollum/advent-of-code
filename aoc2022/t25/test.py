# coding: utf-8
import pytest
from .solution import dec_to_snafu, snafu_to_dec


EXAMPLES = [
    (1, '1'),
    (2, '2'),
    (3, '1='),
    (4, '1-'),
    (5, '10'),
    (6, '11'),
    (7, '12'),
    (8, '2='),
    (9, '2-'),
    (10, '20'),
    (11, '21'),
    (15, '1=0'),
    (20, '1-0'),
    (31, '111'),
    (32, '112'),
    (37, '122'),
    (107, '1-12'),
    (198, '2=0='),
    (201, '2=01'),
    (353, '1=-1='),
    (906, '12111'),
    (1257, '20012'),
    (1747, '1=-0-2'),
    (2022, '1=11-2'),
    (12345, '1-0---0'),
    (314159265, '1121-1110-1=0')
]


@pytest.mark.parametrize('number, expected', EXAMPLES)
def test_dec_to_snafu(number, expected):
    assert dec_to_snafu(number) == expected


@pytest.mark.parametrize('number, expected', [(i[1], i[0]) for i in EXAMPLES])
def test_snafu_to_dec(number, expected):
    assert snafu_to_dec(number) == expected
