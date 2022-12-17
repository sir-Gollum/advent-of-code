# coding: utf-8
import sys
from functools import reduce

from aocutils.iteration import chunkwise


def ch_score(ch):
    if 'a' <= ch <= 'z':
        return ord(ch) - ord('a') + 1
    else:
        return ord(ch) - ord('A') + 27


def main(input_file_name):
    answer1 = 0

    with open(input_file_name) as f:
        lines = [l.strip() for l in f]

    for line in lines:
        mid = len(line.strip()) // 2
        left = line[:mid]
        right = line[mid:]

        common = set(left) & set(right)
        assert len(common) == 1
        answer1 += ch_score(common.pop())

    print('Answer 1:', answer1)

    answer2 = 0
    for group in chunkwise(lines, 3):
        group_elements = [set(it) for it in group]
        common = reduce(lambda x, y: x & y, group_elements)
        assert len(common) == 1
        answer2 += ch_score(common.pop())

    print('Answer 2:', answer2)


if __name__ == '__main__':
    main(sys.argv[1])
