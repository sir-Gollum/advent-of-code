# coding: utf-8
import argparse
import itertools
from functools import cmp_to_key
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


class RightOrder(ValueError):
    pass


class WrongOrder(ValueError):
    pass


def _check_order(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left > right:
            raise WrongOrder(f'Int wrong order: {left} > {right}')
        if left < right:
            raise RightOrder(f'Int right order: {left} < {right}')
        return

    if isinstance(left, list) and isinstance(right, list):
        for ll, rl in itertools.zip_longest(left, right, fillvalue=None):
            if ll is None and rl is not None:
                raise RightOrder(
                    f'List right order: len({left})={len(left)} < len({right})={len(right)}'
                )
            if rl is None and ll is not None:
                raise WrongOrder(
                    f'List wrong order: len({left})={len(left)} > len({right})={len(right)}'
                )
            _check_order(ll, rl)
        log.debug(f'Lists edge case: len({left})={len(left)} == len({right})={len(right)}')
        return

    if isinstance(left, int) and isinstance(right, list):
        _check_order([left], right)

    if isinstance(left, list) and isinstance(right, int):
        _check_order(left, [right])

    log.debug('Edge case: undecided and reached the end')


def check_order(left, right):
    try:
        log.debug(f'=========\nChecking packets \nL: {left} \nR: {right}')
        _check_order(left, right)
        log.debug('Undecided\n')
        return 0
    except RightOrder as e:
        log.debug(f'Packets are in the right order: {e}\n')
        return 1
    except WrongOrder as e:
        log.debug(f'Packets are in the wrong order: {e}\n')
        return -1


def main(input_file_name):
    packets = []
    all_packets = [[[6]], [[2]]]
    with open(input_file_name) as f:
        for pair in f.read().split("\n\n"):
            left, right = map(eval, pair.strip().split("\n"))
            packets.append((left, right))
            all_packets.append(left)
            all_packets.append(right)

    answer1 = 0
    for n, (left, right) in enumerate(packets):
        if check_order(left, right) == 1:
            answer1 += n + 1

    all_packets.sort(key=cmp_to_key(check_order), reverse=True)
    answer2 = (all_packets.index([[2]]) + 1) * (all_packets.index([[6]]) + 1)

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
