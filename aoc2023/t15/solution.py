# coding: utf-8
import argparse
import dataclasses
import re
from collections import defaultdict
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


@dataclasses.dataclass
class B:
    labels: set = dataclasses.field(default_factory=set)
    lenses: list = dataclasses.field(default_factory=list)


def compute_hash(data: str) -> int:
    v = 0
    for ch in data:
        v += ord(ch)
        v *= 17
        v %= 256
    return v


def main(input_file_name):
    with open(input_file_name) as f:
        data = f.read().strip().split(',')

    answer1 = sum(compute_hash(it) for it in data)

    boxes = defaultdict(B)
    for it in data:
        label, op, focal_length = re.split(r'([-=])', it)
        box_idx = compute_hash(label)
        if op == '-':
            if label in boxes[box_idx].labels:
                boxes[box_idx].labels.remove(label)
                for lens in boxes[box_idx].lenses:
                    if lens[0] == label:
                        boxes[box_idx].lenses.remove(lens)
        else:
            if label in boxes[box_idx].labels:
                for lens in boxes[box_idx].lenses:
                    if lens[0] == label:
                        lens[1] = focal_length
            else:
                boxes[box_idx].labels.add(label)
                boxes[box_idx].lenses.append([label, focal_length])

        debug = {k: v.lenses for k, v in boxes.items()}
        log.debug(f'After {it}: \n{debug}')

    answer2 = 0
    for box_idx, box in boxes.items():
        for lens_idx, lens in enumerate(box.lenses):
            answer2 += (box_idx + 1) * (lens_idx + 1) * int(lens[1])

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
