# coding: utf-8
import re
import sys
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO
from aocutils.iteration import chunkwise

log = getLogger(__name__)


def parse(file_name):
    num_stacks = 0
    expected_len = 0
    with open(file_name) as f:
        lines = [line.rstrip() for line in f]

    for line in lines:
        if line.startswith(' 1 '):
            num_stacks = int(line.split(' ')[-1])
            expected_len = num_stacks * 3 + num_stacks
            break

    log.debug('Will have %s stacks, expected line len: %s', num_stacks, expected_len)
    stacks = [[] for _ in range(num_stacks)]
    instructions = []

    for line in lines:
        if not line.strip():
            continue

        if '[' in line:
            line = line.ljust(expected_len)
            for stack_idx, chunk in enumerate(chunkwise(line, 4)):
                if not chunk.strip():
                    continue

                ch = chunk.strip().lstrip('[').rstrip(']')
                stacks[stack_idx].append(ch)
            continue

        m = re.match(r'move (\d+) from (\d+) to (\d+)', line)
        if m:
            count, fr, to = map(int, m.groups())
            instructions.append((count, fr, to))

    stacks = [list(reversed(st)) for st in stacks]
    return stacks, instructions


def process_instructions(stacks, instructions, do_reverse):
    for count, fr, to in instructions:
        log.debug('Stacks before: %s', stacks)
        log.debug('Moving %s from %s to %s', count, fr, to)
        fr_idx = fr - 1
        to_idx = to - 1

        moved = stacks[fr_idx][-count:]
        stacks[fr_idx] = stacks[fr_idx][:-count]

        if do_reverse:
            moved = list(reversed(moved))

        stacks[to_idx].extend(moved)
    return stacks


def main(input_file_name):
    stacks, instructions = parse(input_file_name)
    log.debug("stacks: %s", stacks)
    log.debug("instructions: %s", instructions)

    stacks = process_instructions(stacks, instructions, True)
    answer1 = ''.join([st[-1] for st in stacks if st])

    stacks, instructions = parse(input_file_name)
    stacks = process_instructions(stacks, instructions, False)
    answer2 = ''.join([st[-1] for st in stacks if st])

    log.info('Answer 1: %s', answer1)
    log.info('Answer 2: %s', answer2)


if __name__ == '__main__':
    configure_logging(INFO)
    main(sys.argv[1])
