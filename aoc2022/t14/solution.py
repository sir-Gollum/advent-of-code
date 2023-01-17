# coding: utf-8
import argparse
import os
from logging import getLogger
from time import sleep

from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


HOLE_X, HOLE_Y = 500, 0


def coord_range(a, b):
    if a is None:
        return range(b, b + 1)
    return range(min(a, b), max(a, b) + 1)


def get_borders(rocks, pad=0):
    min_x, max_x, min_y, max_y = 10**10, 0, 10**10, 0

    for x, y in rocks:
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    min_x = min(min_x, HOLE_X)
    max_x = max(max_x, HOLE_X)
    min_y = min(min_y, HOLE_Y)
    max_y = max(max_y, HOLE_Y)

    min_x -= pad
    min_y -= pad
    max_x += pad
    max_y += pad
    return min_x, min_y, max_x, max_y


def vis(rocks, sand, pad=0):
    min_x, min_y, max_x, max_y = get_borders(rocks, pad=pad)
    log.debug(f'min_x: {min_x} min_y: {min_y} max_x: {max_x} max_y: {max_y}')
    result = []
    for y in coord_range(min_y, max_y):
        row = []
        for x in coord_range(min_x, max_x):
            if (x, y) in rocks:
                row.append('#')
            elif (x, y) in sand:
                row.append('o')
            elif (x, y) == (HOLE_X, HOLE_Y):
                row.append('+')
            else:
                row.append('.')
        result.append(''.join(row))
    return '\n'.join(result)


def animation_frame(rocks, sand, pad):
    _ = os.system('clear')
    log.info(vis(rocks, sand, pad))
    sleep(0.03)


def sim(rocks, pad=0, is_part2=False, animate=False):
    min_x, min_y, max_x, max_y = get_borders(rocks)
    sand = set()

    path = [(HOLE_X, HOLE_Y)]
    while True:
        if is_part2 and (HOLE_X, HOLE_Y) in sand:
            return len(sand)

        sx, sy = path[-1]
        while True:
            if animate:
                animation_frame(rocks, sand | {(sx, sy)}, pad)

            occupied = rocks | sand
            if not is_part2 and (sx < min_x or sx > max_x or sy < min_y or sy > max_y):
                return len(sand)

            part2_cond = not is_part2 or sy < max_y + 1
            c_fall_down = (sx, sy + 1)
            if c_fall_down not in occupied and part2_cond:
                sx, sy = c_fall_down
                path.append((sx, sy))
                continue

            c_slide_left = (sx - 1, sy + 1)
            if c_slide_left not in occupied and part2_cond:
                sx, sy = c_slide_left
                path.append((sx, sy))
                continue

            c_slide_right = (sx + 1, sy + 1)
            if c_slide_right not in occupied and part2_cond:
                sx, sy = c_slide_right
                path.append((sx, sy))
                continue

            sand.add((sx, sy))
            path.pop()
            break


def main(input_file_name, is_part2, animate):
    rocks = set()
    with open(input_file_name) as f:
        for line in f:
            points = line.strip().split(' -> ')
            prev_x, prev_y = None, None
            for point in points:
                x, y = map(int, point.split(','))
                for tx in coord_range(prev_x, x):
                    for ty in coord_range(prev_y, y):
                        rocks.add((tx, ty))
                prev_x, prev_y = x, y

    log.debug(f'Rocks: \n{vis(rocks, {})}')
    if not is_part2:
        answer1 = sim(rocks, animate=animate)
        print('Answer 1:', answer1)
    else:
        answer2 = sim(rocks, pad=10, is_part2=is_part2, animate=animate)
        print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-a', '--animate', action='store_true')
    parser.add_argument('-2', '--part2', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename, args.part2, args.animate)
