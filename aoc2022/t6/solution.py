# coding: utf-8
import sys


def find_start_marker_idx(stream: str, distinct_chars: int):
    buf = []
    for idx, ch in enumerate(stream):
        buf.append(ch)
        if idx < distinct_chars-1:
            continue
        buf = buf[-distinct_chars:]

        if len(set(buf)) == distinct_chars:
            return idx + 1

    return -1


def main(input_file_name):
    stream = open(input_file_name).read().strip()
    answer1 = find_start_marker_idx(stream, 4)
    answer2 = find_start_marker_idx(stream, 14)
    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    main(sys.argv[1])
