# coding: utf-8
import argparse
from collections import deque
from logging import getLogger

import tqdm

from aocutils.debug import configure_logging, DEBUG, INFO, colors
from aocutils.grids import LineGrid

log = getLogger()


R = 'R'
L = 'L'
U = 'U'
D = 'D'


DIRECTIONS = {
    U: (-1, 0),
    D: (1, 0),
    L: (0, -1),
    R: (0, 1),
}


def plot_energized(grid: LineGrid, energized):
    rg = LineGrid.from_linegrid(grid)
    for ridx in range(rg.rows):
        for cidx in range(rg.cols):
            if (ridx, cidx) in energized:
                rg.g[ridx][cidx] = colors.RED + rg.g[ridx][cidx] + colors.ENDC
    log.debug(rg)


def simulate_energized(
    g: LineGrid,
    start_pos: (int, int) = (0, -1),
    start_direction: str = R
) -> int:
    res = set()
    visited = set()
    queue = deque([(start_pos, start_direction)])

    while queue:
        pos, direction = queue.pop()
        if g.is_coord_in_grid(*pos):
            res.add(pos)

        dd = DIRECTIONS[direction]
        next_pos = (pos[0] + dd[0], pos[1] + dd[1])

        if g.is_coord_in_grid(*pos) and not g.is_coord_in_grid(*next_pos):
            continue

        if (pos, direction) in visited:
            log.debug(f'\n\nGlobally seen: {pos}, {direction}. Visited: {visited}')
            continue

        visited.add((pos, direction))
        next_ch = g.g[next_pos[0]][next_pos[1]]

        if next_ch == '|':
            if direction in {U, D}:
                queue.append((next_pos, direction))
            else:
                queue.append((next_pos, U))
                queue.append((next_pos, D))
        elif next_ch == '-':
            if direction in {L, R}:
                queue.append((next_pos, direction))
            else:
                queue.append((next_pos, L))
                queue.append((next_pos, R))
        elif next_ch == '\\':
            if direction == R:
                queue.append((next_pos, D))
            elif direction == L:
                queue.append((next_pos, U))
            elif direction == U:
                queue.append((next_pos, L))
            else:
                queue.append((next_pos, R))
        elif next_ch == '/':
            if direction == R:
                queue.append((next_pos, U))
            elif direction == L:
                queue.append((next_pos, D))
            elif direction == U:
                queue.append((next_pos, R))
            else:
                queue.append((next_pos, L))
        else:
            queue.append((next_pos, direction))

    log.debug('\n\nEnergized: %s\n\n', res)
    plot_energized(g, res)
    return len(res)


def main(input_file_name):
    with open(input_file_name) as f:
        g = LineGrid.from_lines(f.read().splitlines())

    log.debug(g)

    answer1 = simulate_energized(g)

    params2 = [
        ((r, -1), R) for r in range(g.rows)
    ] + [
        ((r, g.cols), L) for r in range(g.rows)
    ] + [
        ((-1, c), D) for c in range(g.cols)
    ] + [
        ((g.rows, c), U) for c in range(g.cols)
    ]
    answer2 = 0
    for p in tqdm.tqdm(params2):
        answer2 = max(answer2, simulate_energized(g, *p))

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
