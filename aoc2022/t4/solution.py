# coding: utf-8
import re
import sys


def fully_contains(a, b):
    return (
        a[0] >= b[0] and a[1] <= b[1]
    ) or (
        b[0] >= a[0] and b[1] <= a[1]
    )


def overlaps(a, b):
    return (
      b[0] <= a[0] <= b[1]
      or
      b[0] <= a[1] <= b[1]
      or
      a[0] <= b[0] <= a[1]
      or
      a[0] <= b[1] <= a[1]
    )


def main(input_file_name):
    answer1 = 0
    answer2 = 0
    for line in open(input_file_name):
        m = re.match(r'(\d+)-(\d+),(\d+)-(\d+)', line.strip())
        fr1, to1, fr2, to2 = map(int, m.groups())

        answer1 += int(fully_contains((fr1, to1), (fr2, to2)))
        answer2 += int(overlaps((fr1, to1), (fr2, to2)))

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    main(sys.argv[1])
