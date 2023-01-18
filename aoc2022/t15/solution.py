# coding: utf-8
import argparse
import re
from dataclasses import dataclass
from logging import getLogger
from tqdm import tqdm
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


@dataclass
class Sensor:
    pos: complex
    beacon: complex


def manhattan(a, b):
    return abs(a.real - b.real) + abs(a.imag - b.imag)


def merge_ranges(ranges):
    # based on https://codereview.stackexchange.com/questions/69242/merging-overlapping-intervals
    merged = []

    for higher in sorted(ranges):
        if not merged:
            merged.append(higher)
        else:
            lower = merged[-1]
            # test for intersection between lower and higher, or they are adjacent:
            # we know via sorting that lower[0] <= higher[0]
            if higher[0] <= lower[1] + 1:  # (+1 for adjacency)
                upper_bound = max(lower[1], higher[1])
                merged[-1] = (lower[0], upper_bound)
            else:
                merged.append(higher)
    return merged


def check_line(sensors, line_to_check, is_example=False):
    """
    Returns:
         - a list of ranges where there can't be beacons
         - number of cells where there can't be beacons (answer1)
    """
    ranges_on_line = []
    for s in sensors:
        md = manhattan(s.pos, s.beacon)
        if not (s.pos.imag - md <= line_to_check <= s.pos.imag + md):
            continue

        dist_to_line = abs(line_to_check - s.pos.imag)
        line_range = (
            int(s.pos.real - md + dist_to_line),
            int(s.pos.real + md - dist_to_line),
        )
        ranges_on_line.append(line_range)
        log.debug(
            f'Sensor {s} with MD {md} affects line '
            f'{line_to_check} \n\t with distance {dist_to_line} and range (incl.) {line_range}'
        )

    mr = merge_ranges(ranges_on_line)
    log.debug('Merged ranges: %s\n', mr)
    if not is_example:
        return mr, None, None

    beacons_excluded = set()
    for s in sensors:
        if s.beacon.imag == line_to_check:
            if any([r[0] <= s.beacon.real <= r[1] for r in mr]):
                log.debug(f"Sensor {s}'s beacon is in line we check and in merged ranges")
                beacons_excluded.add(s.beacon)

    return mr, sum([r[1] - r[0] + 1 for r in mr]) - len(beacons_excluded)


def main(input_file_name, is_example=False):
    line_to_check = 10 if is_example else 2000000
    coord_limit = 20 if is_example else 4000000
    log.debug(f"Will check line: {line_to_check}, coordinates limit: {coord_limit}")

    sensors = []
    with open(input_file_name) as f:
        for line in f:
            line = line.strip()
            m = re.match(
                r"Sensor at x=([^,]+), y=([^,]+): closest beacon is at x=([^,]+), y=([^,]+)",
                line
            )
            gr = list(map(int, m.groups()))
            sensors.append(Sensor(
                complex(gr[0], gr[1]),
                complex(gr[2], gr[3])
            ))

    log.debug('Sensors: %s\n', sensors)
    answer1 = check_line(sensors, line_to_check)[1]
    answer2 = -1

    for y in tqdm(range(coord_limit + 1)):
        mr = check_line(sensors, y, is_example)[0]
        if len(mr) > 1:
            x = mr[0][1] + 1  # mr is sorted
            answer2 = x * coord_limit + y
            break

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-e', '--example', action='store_true')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename, args.example)
