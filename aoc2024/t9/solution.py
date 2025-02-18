# coding: utf-8
import argparse
from logging import getLogger
from icecream import ic
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def to_str(data):
    res = []
    for i in range(max(data.keys()) + 1):
        res.append(data.get(i, "."))
    return "".join(map(str, res))


def next_free_space(data, start, space_len=1):
    # short circuit - check first space first
    md = max(data.keys())
    while start < md:
        while start in data and start < md:
            start += 1

        if all(start + i not in data for i in range(space_len)):
            return start
        else:
            start += min(space_len - 1, 1)

    if start >= md:
        return -1
    return start


def last_occupied_space(data, end):
    while end not in data:
        end -= 1
    return end


def last_occupied_file(data, end, skip_file_id=None):
    while end >= 0 and (
        end not in data or (end in data and skip_file_id and data[end] == skip_file_id)
    ):
        end -= 1

    if end < 0:
        return -1, -1

    start = end
    while start in data and data[start] == data[end]:
        start -= 1

    return start + 1, end


def part1(data):
    # move individual blocks
    data = data.copy()
    left = next_free_space(data, 0)
    right = last_occupied_space(data, max(data.keys()) + 1)

    while left != -1 and left < right:
        data[left] = data.pop(right)
        left = next_free_space(data, left)
        right = last_occupied_space(data, right)

    answer = 0
    for i in range(max(data.keys()) + 1):
        answer += i * data[i]
    return answer


def part2(data):
    data = data.copy()
    right_start, right_end = last_occupied_file(data, max(data.keys()) + 1)
    length = right_end - right_start + 1
    ic(to_str(data))

    moved_file_ids = set()

    while right_start > 0:
        skip_file_id = data[right_start]
        if skip_file_id not in moved_file_ids:
            left = next_free_space(data, 0, length)
            ic(left, right_start, right_end, length, skip_file_id)

            if left != -1 and left < right_start:
                for offset in range(length):
                    assert left + offset not in data
                    data[left + offset] = data.pop(right_start + offset)
                    moved_file_ids.add(skip_file_id)

        right_start, right_end = last_occupied_file(data, right_start, skip_file_id)
        length = right_end - right_start + 1

    ic(to_str(data))
    answer = 0
    for i in range(max(data.keys()) + 1):
        answer += i * data.get(i, 0)
    return answer


def main(input_file_name):
    with open(input_file_name) as f:
        input_data = f.read()

    items = list(map(int, input_data.strip()))
    is_file = False
    data = {}
    file_id = 0
    offset = 0

    data2 = {}
    spaces2 = {}

    for block_len in items:
        is_file = not is_file

        if is_file:
            for i in range(block_len):
                data[offset + i] = file_id

            data2[offset] = (block_len, file_id)
            file_id += 1
        else:
            spaces2[offset] = block_len

        offset += block_len

    print("Answer 1:", part1(data))
    print("Answer 2:", part2(data))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()
    configure_logging(DEBUG if args.debug else INFO)
    if not args.debug:
        ic.disable()
    main(args.filename)
