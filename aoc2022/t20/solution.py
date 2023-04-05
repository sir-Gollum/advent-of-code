# coding: utf-8
import argparse
import collections
from logging import getLogger
import tqdm
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def move(items, positions, orig_idx):
    cur_idx = positions.index(orig_idx)

    if items[cur_idx] != '0':
        items.rotate(-cur_idx)
        positions.rotate(-cur_idx)

        v = items.popleft()
        positions.popleft()

        items.rotate(-v)
        positions.rotate(-v)

        items.appendleft(v)
        positions.appendleft(orig_idx)

        extra = -1 if v < 0 else 0

        items.rotate(cur_idx + v + extra)
        positions.rotate(cur_idx + v + extra)

    log.debug('After moving %s:\n%s', v, items)


def mix(items, rounds=1):
    num_items = len(items)
    items = collections.deque(items)
    positions = collections.deque(range(num_items))

    log.debug('Initial:\n%s', items)

    for round in range(rounds):
        for orig_idx in tqdm.tqdm(range(num_items)):
            move(items, positions, orig_idx)

    res_elements = []
    items.rotate(-items.index(0))
    for i in range(3):
        items.rotate(-1000)
        res_elements.append(items[0])

    log.debug(f'Result elemens: {res_elements}')

    return sum(res_elements)


def main(input_file_name):
    with open(input_file_name) as f:
        items = [int(x) for x in f if x.strip()]
        items2 = [x * 811589153 for x in items]

    answer1 = mix(items)
    answer2 = mix(items2, rounds=10)

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
