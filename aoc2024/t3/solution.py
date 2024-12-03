# coding: utf-8
import argparse
import re
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def main(input_file_name):
    answer1 = 0
    answer2 = 0
    mul_enabled = True

    with open(input_file_name) as f:
        for m in re.finditer(
            r"do\(\)"
            r"|don't\(\)"
            r"|mul\((\d+),(\d+)\)",
            f.read()
        ):
            sub = m.string[m.start():m.end()]
            if sub in {"do()", "don't()"}:
                mul_enabled = sub == "do()"
                continue

            a, b = map(int, m.groups())
            answer1 += a * b
            if mul_enabled:
                answer2 += a * b

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
