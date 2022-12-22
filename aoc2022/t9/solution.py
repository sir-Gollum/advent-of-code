# coding: utf-8
import argparse
import os
from logging import getLogger
from time import sleep

from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


# (head x - tail x, head y - tail y) -> (step for tail x, step for tail y)
STEPS = {
    (-2, -2): (-1, -1),
    (-2, -1): (-1, -1),
    (-2, 0): (-1, 0),
    (-2, 1): (-1, 1),
    (-2, 2): (-1, 1),
    (-1, -2): (-1, -1),
    (-1, 2): (-1, 1),
    (0, -2): (0, -1),
    (0, 2): (0, 1),
    (1, -2): (1, -1),
    (1, 2): (1, 1),
    (2, -2): (1, -1),
    (2, -1): (1, -1),
    (2, 0): (1, 0),
    (2, 1): (1, 1),
    (2, 2): (1, 1),
}


def vis(tx, ty, bx, by, knots):
    res = []
    for row_idx, y in enumerate(range(ty, by)):
        res.append([])
        for x in range(tx, bx):
            try:
                m = knots.index((x, y))
                res[row_idx].append(str(m))
            except ValueError:
                res[row_idx].append('.')
    return '\n'.join(''.join(r) for r in res)


def animation_frame(grid_size, knots, direction, distance):
    _ = os.system('clear')
    log.info(vis(-grid_size, -grid_size, grid_size, grid_size, knots))
    log.info('\n== Instruction %s %s == ', direction, distance)
    sleep(0.1)


def simulate(instructions, num_knots, animate=False):
    knots = [(0, 0) for _ in range(num_knots)]
    tail_visited = set()
    grid_size = 15

    for direction, distance in instructions:
        log.debug('\n== %s %s below == ', direction, distance)

        for _ in range(distance):
            hx, hy = knots[0]
            if direction == "R":
                hx += 1
            elif direction == "L":
                hx -= 1
            elif direction == "U":
                hy -= 1
            elif direction == "D":
                hy += 1

            knots[0] = (hx, hy)
            if animate:
                animation_frame(grid_size, knots, direction, distance)

            for i in range(1, num_knots):
                hx, hy = knots[i-1]
                tx, ty = knots[i]

                step = STEPS.get((hx - tx, hy - ty), (0, 0))
                tx += step[0]
                ty += step[1]
                if i == num_knots - 1:
                    tail_visited.add((tx, ty))
                knots[i] = (tx, ty)

                if animate and step != (0, 0):
                    animation_frame(grid_size, knots, direction, distance)

        log.debug(vis(-grid_size, -grid_size, grid_size, grid_size, knots))
    return tail_visited


def main(input_file_name, animate):
    instructions = []
    with open(input_file_name) as f:
        for line in f:
            direction, distance = line.strip().split()
            instructions.append((direction, int(distance)))

    answer1 = len(simulate(instructions, 2))
    answer2 = len(simulate(instructions, 10, animate))

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-a', '--animate', action='store_true')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename, args.animate)
