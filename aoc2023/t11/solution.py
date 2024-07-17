# coding: utf-8
import argparse
import copy
import itertools
from collections import defaultdict
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def manhattan(a: tuple[int, int], b: tuple[int, int]):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def print_galaxies(galaxies: set[tuple[int, int]]):
    a_lot = 10**10
    min_x, min_y, max_x, max_y = a_lot, a_lot, -a_lot, -a_lot

    for x, y in galaxies:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            row.append('#' if (x, y) in galaxies else '.')
        log.debug(''.join(row))
    log.debug('')


def expand(galaxies: set[tuple[int, int]], expansion_factor: int = 1) -> set[tuple[int, int]]:
    new = copy.deepcopy(galaxies)

    rows, cols = defaultdict(set), defaultdict(set)
    for x, y in galaxies:
        rows[y].add(x)
        cols[x].add(y)

    rows_to_expand, cols_to_expand = [], []

    for x in range(min(rows), max(rows) + 1):
        if x not in rows:
            rows_to_expand.append(x)

    for y in range(min(cols), max(cols) + 1):
        if y not in cols:
            cols_to_expand.append(y)

    log.debug('rows_to_expand=%s', rows_to_expand)
    log.debug('cols_to_expand=%s', cols_to_expand)

    for row in reversed(rows_to_expand):
        galaxies_to_push = []
        for (x, y) in new:
            if y > row:
                galaxies_to_push.append((x, y))

        for (x, y) in galaxies_to_push:
            new.remove((x, y))
            new.add((x, y + expansion_factor))

    for col in reversed(cols_to_expand):
        galaxies_to_push = []
        for (x, y) in new:
            if x > col:
                galaxies_to_push.append((x, y))

        for (x, y) in galaxies_to_push:
            new.remove((x, y))
            new.add((x + expansion_factor, y))

    log.debug('new=%s', sorted(new))
    return new


def main(input_file_name):
    galaxies = set()
    with open(input_file_name) as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line.strip()):
                if c == '#':
                    galaxies.add((x, y))

    print_galaxies(galaxies)
    expanded = expand(galaxies)
    print_galaxies(expanded)
    answer1 = sum(manhattan(a, b) for a, b in itertools.combinations(expanded, 2))

    expanded2 = expand(galaxies, 1000000-1)
    answer2 = sum(manhattan(a, b) for a, b in itertools.combinations(expanded2, 2))

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
