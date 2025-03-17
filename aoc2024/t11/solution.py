# coding: utf-8
import argparse
from logging import getLogger

from black.trans import defaultdict
from icecream import ic
from aocutils.debug import configure_logging, DEBUG, INFO


log = getLogger()


def blink(s):
    if s == 0:
        return (1,)
    else:
        strs = str(s)
        ls = len(strs)
        if ls % 2 == 0:
            return int(strs[: ls // 2]), int(strs[ls // 2 :])
        else:
            return (s * 2024,)


def main(input_file_name):
    with open(input_file_name) as f:
        stones = defaultdict(int)
        for s in f.read().split():
            stones[int(s)] += 1

    answer1 = 0
    for i in range(75):
        new_stones = defaultdict(int)
        for k, v in stones.items():
            for new_k in blink(k):
                new_stones[new_k] += v
        stones = new_stones
        if i == 24:
            answer1 = sum(stones.values())

    answer2 = sum(stones.values())
    print("Answer 1:", answer1)
    print("Answer 2:", answer2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()
    configure_logging(DEBUG if args.debug else INFO)
    if not args.debug:
        ic.disable()
    main(args.filename)
