# coding: utf-8
import argparse
from collections import deque
from logging import getLogger

from icecream import ic

from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def is_possible(result: int, operands: list[int], check_concat: bool = False) -> bool:
    queue = deque([(result, 0, operands, [])])

    while queue:
        res, intermediate, ops, ops_history = queue.pop()

        if not ops:
            if res == intermediate:
                return True
            continue

        queue.append((res, intermediate + ops[0], ops[1:], ops_history + ['+']))
        queue.append((res, intermediate * ops[0], ops[1:], ops_history + ['*']))
        if check_concat:
            queue.append((res, int(str(intermediate) + str(ops[0])), ops[1:], ops_history + ['||']))

    return False


def main(input_file_name):
    operators = []
    with open(input_file_name) as f:
        for line in f:
            result, operands = line.split(': ')
            result = int(result)
            operands = [int(x) for x in operands.split()]
            operators.append((result, operands))

    ic(operators)

    answer1, answer2 = 0, 0
    for result, operands in operators:
        if is_possible(result, operands):
            answer1 += result

        if is_possible(result, operands, True):
            answer2 += result

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
