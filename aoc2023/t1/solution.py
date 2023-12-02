# coding: utf-8
import argparse
import string
import re
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()

LITERALS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

regex = re.compile('(?=(' + '|'.join(list(LITERALS.keys()) + list(string.digits)) + '))')


def main(input_file_name):
    log.debug('Regex: %s', regex)
    answer1, answer2 = 0, 0
    with open(input_file_name) as f:
        for line in f:
            matches = [m.group(1) for m in regex.finditer(line.strip())]

            assert len(matches) > 0, f'0 matches in "{line}"'
            digit_matches = [m for m in matches if len(m) == 1]
            p1_first, p1_last = '0', '0'
            if digit_matches:
                p1_first = digit_matches[0]
                p1_last = digit_matches[-1]

            p2_first = LITERALS.get(matches[0], matches[0])
            p2_last = LITERALS.get(matches[-1], matches[-1])

            log.debug(f'{line.strip()} -> {p2_first + p2_last} | {matches}')
            answer1 += int(p1_first + p1_last)
            answer2 += int(p2_first + p2_last)

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
