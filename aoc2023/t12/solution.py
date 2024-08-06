# coding: utf-8
import argparse
import functools
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def count_broken(springs: str, groups: tuple[int], gr: int) -> int:
    if len(springs) < gr:
        return 0

    if springs[:gr].replace('?', '#') != '#' * gr:
        return 0

    if len(springs) == gr:
        return 1 if len(groups) == 1 else 0

    if springs[gr] in {'.', '?'}:
        return count_combinations(springs[gr + 1:], groups[1:])

    return 0


def count_gap(springs: str, groups: tuple[int]):
    return count_combinations(springs[1:], groups)


@functools.lru_cache
def count_combinations(springs: str, groups: tuple[int]) -> int:
    if not groups:
        return 1 if '#' not in springs else 0

    if not springs:
        return 0

    ch, gr = springs[0], groups[0]

    if ch == '.':
        return count_gap(springs, groups)

    if ch == '#':
        return count_broken(springs, groups, gr)

    if ch == '?':
        return count_gap(springs, groups) + count_broken(springs, groups, gr)

    raise ValueError(f'Unexpected character: {ch}')


def main(input_file_name):
    inp = []
    with open(input_file_name) as f:
        for line in f:
            springs, groups = line.strip().split()
            groups = tuple(map(int, groups.split(',')))
            inp.append((springs, groups))

    log.debug('==== Part 1 ====')
    answer1 = 0
    for sprin_gs, groups in inp:
        cmb = count_combinations(sprin_gs, groups)
        log.debug('%s %s --> %s', sprin_gs, groups, cmb)
        answer1 += cmb

    log.debug('==== Part 2 ====')
    answer2 = 0
    for springs, groups in inp:
        springs = '?'.join([springs for _ in range(5)])
        groups = tuple(sum([list(groups) for _ in range(5)], []))
        cmb = count_combinations(springs, groups)
        log.debug('%s %s --> %s', springs, groups, cmb)
        answer2 += cmb

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
