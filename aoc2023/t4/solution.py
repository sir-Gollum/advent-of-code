# coding: utf-8
import argparse
from logging import getLogger
from collections import defaultdict
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def main(input_file_name):
    answer1, answer2 = 0, 0
    copies = defaultdict(lambda: 1)

    with open(input_file_name) as f:
        for line in f:
            line = line.strip()
            card_text, numbers = line.split(': ')
            card_number = int(card_text.split()[1])
            parts = numbers.strip().split(' | ')
            winning_numbers = {int(n) for n in parts[0].split()}

            # part 1 (mostly)
            card_points = 0
            matching_numbers = 0
            for n in [int(n) for n in parts[1].split()]:
                if n in winning_numbers:
                    matching_numbers += 1
                    if not card_points:
                        card_points = 1
                    else:
                        card_points *= 2
            answer1 += card_points

            # part 2
            if matching_numbers:
                for i in range(1, matching_numbers + 1):
                    copies[card_number + i] += copies[card_number]
            answer2 += copies[card_number]

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
