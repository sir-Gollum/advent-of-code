# coding: utf-8
import pytest
from .solution import Mapping, Range


@pytest.mark.parametrize(
    'mapping, rng, expected_converted, expected_unconverted',
    [
        # example 1 step (seed-to-soil)
        (
            Mapping(dst_start=52, src_start=50, length=48),
            Range(79, 14),
            Range(81, 14),
            None,
        ),
        (
            Mapping(52, 50, 48),
            Range(55, 13),
            Range(57, 13),
            None,
        ),
        # example 2 step, range 1 (soil-to-fertilizer)
        (
            Mapping(0, 15, 37),
            Range(81, 14),
            None,
            Range(81, 14),
        ),
        (
            Mapping(37, 52, 2),
            Range(81, 14),
            None,
            Range(81, 14),
        ),
        (
            Mapping(39, 0, 15),
            Range(81, 14),
            None,
            Range(81, 14),
        ),
        # example 2 step, range 2
        (
            Mapping(0, 15, 37),
            Range(57, 13),
            None,
            Range(57, 13),
        ),
        (
            Mapping(37, 52, 2),
            Range(57, 13),
            None,
            Range(57, 13),
        ),
        (
            Mapping(39, 0, 15),
            Range(57, 13),
            None,
            Range(57, 13),
        ),
        # example 3 step (fertilizer-to-water)
        (
            Mapping(49, 53, 8),
            Range(57, 13),
            Range(53, 4),
            Range(61, 9),
        ),
        # at end of step 3, ranges: (53, 4), (61, 9), (81, 14)
        # example 4 step (water-to-light)
        (
            Mapping(88, 18, 7),
            Range(53, 4),
            None,
            Range(53, 4),
        ),
        (
            Mapping(88, 18, 7),
            Range(61, 9),
            None,
            Range(61, 9),
        ),
        (
            Mapping(88, 18, 7),
            Range(81, 14),
            None,
            Range(81, 14),
        ),
        (
            Mapping(18, 25, 70),
            Range(53, 4),
            Range(46, 4),
            None,
        ),
        (
            Mapping(18, 25, 70),
            Range(61, 9),
            Range(54, 9),
            None,
        ),
        (
            Mapping(18, 25, 70),
            Range(81, 14),
            Range(74, 14),
            None,
        ),
        # at end of step 4, ranges:
        # Range(start=54, length=9), Range(start=74, length=14), Range(start=46, length=4)
        # example 4 step (light-to-temperature)
        (
            Mapping(81, 45, 19),
            Range(54, 9),
            Range(90, 9),
            None,
        ),
        (
            Mapping(45, 77, 23),
            Range(74, 14),
            Range(45, 11),
            Range(74, 3),
        ),
    ]
)
def test_convert_range(mapping, rng, expected_converted, expected_unconverted):
    converted, unconverted = mapping.convert_range(rng)
    assert converted == expected_converted
    assert unconverted == expected_unconverted
