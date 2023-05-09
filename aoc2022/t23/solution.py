# coding: utf-8
import argparse
import collections
import copy
from logging import getLogger
from math import inf
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def bounding_box(positions):
    min_x, max_x, min_y, max_y = inf, -inf, inf, -inf
    for pos in positions:
        min_x = min(min_x, pos.real)
        max_x = max(max_x, pos.real)
        min_y = min(min_y, pos.imag)
        max_y = max(max_y, pos.imag)

    return map(int, (min_x, max_x, min_y, max_y))


def vis(positions):
    min_x, max_x, min_y, max_y = bounding_box(positions)
    rows = []
    for y in range(min_y, max_y+1):
        cols = []
        for x in range(min_x, max_x + 1):
            v = '#' if complex(x, y) in positions else '.'
            cols.append(v)
        rows.append(''.join(cols))
    log.debug('\n'.join(rows) + '\n')


def adjacent(pos, offset=0):
    n = [pos - 1-1j, pos - 1j, pos + 1-1j]
    s = [pos - 1+1j, pos + 1j, pos + 1+1j]
    w = [pos - 1 - 1j, pos - 1, pos - 1+1j]
    e = [pos + 1 - 1j, pos + 1, pos + 1+1j]

    # [[[coordinates_in_the_direction], new_position], ...]
    res =  collections.deque([
        [n, pos - 1j],
        [s, pos + 1j],
        [w, pos - 1],
        [e, pos + 1],
    ])

    res.rotate(-offset)
    return res, n + s + w + e


def simulate(positions, rounds=10):
    positions = copy.deepcopy(positions)
    log.debug('== Simulating...Initial state: ==')
    vis(positions)
    rnd = 0
    for rnd in range(rounds):
        moves_this_round = 0
        proposed = collections.defaultdict(list)

        for pos in positions:
            adj, all_adjacent = adjacent(pos, offset=rnd)

            if all(p not in positions for p in all_adjacent):
                # no elves around, do nothing
                continue

            for positions_to_check, new_pos in adj:
                if all(p not in positions for p in positions_to_check):
                    proposed[new_pos].append(pos)
                    break

        for new_pos, candidates in proposed.items():
            if len(candidates) == 1:
                moves_this_round += 1
                positions.add(new_pos)
                positions.remove(candidates[0])

        if moves_this_round == 0:
            log.debug('== End of Round %d, No moves ths round ==' % (rnd + 1))
            break
        else:
            log.debug(
                '== End of Round %d: (moves ths round: %s) ==' % (rnd + 1, moves_this_round))
            vis(positions)

    min_x, max_x, min_y, max_y = bounding_box(positions)
    log.debug('X: [%s, %s], Y: [%s, %s]' % (min_x, max_x, min_y, max_y))
    vis(positions)
    return (
        (max_x - min_x + 1) * (max_y - min_y + 1) - len(positions),
        rnd + 1
    )


def main(input_file_name):
    positions = set()
    with open(input_file_name) as f:
        for y, line in enumerate(f.read().strip().splitlines()):
            for x, ch in enumerate(line):
                if ch == '#':
                    positions.add(complex(x, y))

    answer1 = simulate(positions, rounds=10)[0]
    answer2 = simulate(positions, rounds=10000)[1]

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
