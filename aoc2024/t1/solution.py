# coding: utf-8
import argparse
from collections import Counter
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def main(input_file_name):
    left, right = [], []
    with open(input_file_name) as f:
        for line in f:
            l, r = map(int, line.strip().split())
            left.append(l)
            right.append(r)

    cr = Counter(right)

    answer1 = 0
    answer2 = 0
    for l, r in zip(sorted(left), sorted(right)):
        dist = abs(l - r)
        sim = l * cr.get(l, 0)
        answer1 += dist
        answer2 += sim
        log.debug(f'{l}, {r} -> {dist}, {sim}')


    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
