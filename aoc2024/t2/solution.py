# coding: utf-8
import argparse
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO
from aocutils.iteration import sliding_window

log = getLogger()


def is_safe(nums):
    deltas = [b - a for a, b in sliding_window(nums, 2)]

    return (
        all(0 < d <= 3 for d in deltas)
        or all(-3 <= d < 0 for d in deltas)
    )


def main(input_file_name):
    answer1 = 0
    answer2 = 0

    with open(input_file_name) as f:
        for line in f:
            nums = list(map(int, line.strip().split()))

            if is_safe(nums):
                answer1 += 1
                answer2 += 1
            else:
                for i, _ in enumerate(nums):
                    if is_safe(nums[:i] + nums[i + 1:]):
                        answer2 += 1
                        break

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
