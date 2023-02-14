# coding: utf-8
import argparse
import collections
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def get_adjacent_coords(x, y, z):
    return {
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    }


def outer_fill(cells):
    min_max = {
        axis: (
            # with a gap around the object
            min(cells, key=lambda p: p[axis])[axis] - 1,
            max(cells, key=lambda p: p[axis])[axis] + 1
        ) for axis in range(3)
    }

    def _is_within_bounds(cell):
        for axis in range(3):
            if cell[axis] < min_max[axis][0] or new_cell[axis] > min_max[axis][1]:
                return False
        return True

    log.debug('Min/Max per axis: %s', min_max)

    start_cell = (min_max[0][0], min_max[1][0], min_max[2][0])
    fill = set(start_cell)
    queue = collections.deque([start_cell])

    while queue:
        cell = queue.popleft()

        for new_cell in get_adjacent_coords(*cell):
            if not _is_within_bounds(new_cell):
                continue

            if new_cell in fill or new_cell in cells:
                continue

            fill.add(new_cell)
            queue.append(new_cell)

    return fill


def main(input_file_name):
    cells = set()

    with open(input_file_name) as f:
        for line in f:
            cell = tuple(map(int, line.strip().split(",")))
            cells.add(cell)

    exposures = {}
    for c in cells:
        exposures[c] = len(get_adjacent_coords(*c).difference(cells))
    answer1 = sum(exposures.values())

    steam = outer_fill(cells)
    outer_exposures = {}
    for c in cells:
        outer_exposures[c] = len(get_adjacent_coords(*c) & steam)
    answer2 = sum(outer_exposures.values())

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
