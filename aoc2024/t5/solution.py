# coding: utf-8
import argparse
from collections import defaultdict
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def is_valid(page, rules):
    for n, it in enumerate(page):
        printed_before = set(page[:n])
        if printed_before & rules[it]:
            return False

    return True


def reorder(page, rules):
    new = page[:]

    ordered = False
    while not ordered:
        for n, it in enumerate(new):
            printed_before = set(new[:n])
            if printed_before & rules[it]:
                # there will only be 1 breaking element at any point
                breaking = (printed_before & rules[it]).pop()
                breaking_idx = new.index(breaking)
                new[n], new[breaking_idx] = new[breaking_idx], new[n]
                break
        else:
            ordered = True

    return new


def main(input_file_name):
    rules = defaultdict(set)
    pages = []
    with open(input_file_name) as f:
        content_rules, content_pages = f.read().strip().split('\n\n')

        for line in content_rules.split('\n'):
            fr, to = map(int, line.split('|'))
            rules[fr].add(to)

        for line in content_pages.split('\n'):
            pages.append(list(map(int, line.split(','))))

    answer1, answer2 = 0, 0
    for page in pages:
        if is_valid(page, rules):
            answer1 += page[len(page) // 2]
        else:
            answer2 += reorder(page, rules)[len(page) // 2]

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
