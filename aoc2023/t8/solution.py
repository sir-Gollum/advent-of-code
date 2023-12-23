# coding: utf-8
import argparse
import itertools
import math
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def part1(instructions, nodes):
    cycled_instructions = itertools.cycle(instructions)
    steps = 0
    cur = 'AAA'
    for inst in cycled_instructions:
        steps += 1
        index = 0 if inst == 'L' else 1
        cur = nodes[cur][index]
        if cur == 'ZZZ':
            break
    return steps


def get_cycle(n, instructions, nodes):
    finishes = []
    cycled_instructions = itertools.cycle(instructions)

    steps = 0
    cur = n
    for inst in cycled_instructions:
        steps += 1
        index = 0 if inst == 'L' else 1
        cur = nodes[cur][index]
        if cur.endswith('Z'):
            finishes.append(steps)
            if len(finishes) == 3:
                break

    log.debug(f'Finishes for {n}: {finishes}')
    assert finishes[0] == finishes[1] - finishes[0]
    assert finishes[0] == finishes[2] - finishes[1]
    return finishes[0]


def part2(instructions, nodes):
    cur_nodes = [n for n in nodes if n.endswith("A")]
    cycles = [get_cycle(n, instructions, nodes) for n in cur_nodes]
    log.debug(f'Cycles: {cycles}')
    return math.lcm(*cycles)


def main(input_file_name):
    with open(input_file_name) as f:
        instructions, node_descriptions = f.read().strip().split('\n\n')

    instructions = instructions.strip()

    nodes = {}
    for line in node_descriptions.split('\n'):
        key, lr = line.split(' = ')
        left, right = lr.replace('(', '').replace(')', '').strip().split(', ')
        nodes[key] = (left, right)

    log.debug(f'Instructions: {instructions}\nNodes: {nodes}')
    answer1 = part1(instructions, nodes)
    answer2 = part2(instructions, nodes)

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
