# coding: utf-8
import argparse
from functools import reduce
from logging import getLogger
from operator import add

from aocutils.debug import configure_logging, DEBUG, INFO
from aocutils.iteration import chunkwise

log = getLogger()


def main(input_file_name):
    def _check_signal_strength():
        if cycle == 20 or (cycle - 20) % 40 == 0:
            signal_strengths.append(cycle * x)

    def _draw():
        display.append(
            '#' if x % 40 - 1 <= (cycle % 40) <= x + 1 else '.'
        )

    display = []
    x = 1
    cycle = 0
    signal_strengths = []
    with open(input_file_name) as f:
        for line in f:
            line = line.strip()
            if line == 'noop':
                _draw()
                cycle += 1
                _check_signal_strength()
            if line.startswith("addx"):
                _draw()
                cycle += 1
                _check_signal_strength()
                _draw()
                cycle += 1
                _check_signal_strength()
                x += int(line.split()[-1])

    log.debug('Cycles: %s, Signal strengths: %s', cycle, signal_strengths)
    answer1 = reduce(add, signal_strengths)
    answer2 = '\n'.join(''.join(line) for line in list(chunkwise(display, 40)))

    print('Answer 1:', answer1)
    print(f'Answer 2:\n{answer2}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
