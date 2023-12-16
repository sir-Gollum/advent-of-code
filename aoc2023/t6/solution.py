# coding: utf-8
import argparse
import operator
from functools import reduce
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def get_num_winning_strategies(race_time: int, record_distance: int) -> int:
    left, right = 0, race_time

    for charge_time in range(1, race_time):
        distance = (race_time - charge_time) * charge_time
        if distance > record_distance:
            left = charge_time
            log.debug('Winning strategy left: %s', left)
            break

    for charge_time in range(race_time, 1, -1):
        distance = (race_time - charge_time) * charge_time
        if distance > record_distance:
            right = charge_time + 1
            log.debug('Winning strategy right: %s', left)
            break

    log.debug(
        'Winning strategies range for t=%s, d=%s: %s | %s', race_time, record_distance, left, right
    )

    return right - left


def main(input_file_name):
    with open(input_file_name) as f:
        lines = f.readlines()
        times, distances = [list(map(int, line.strip().split()[1:])) for line in lines]
        log.debug('Initial times: %s', times)
        log.debug('Initial distances: %s', distances)

        time2, distance2 = [int(''.join(line.strip().split()[1:])) for line in lines]
        log.debug('Initial time (part 2): %s', time2)
        log.debug('Initial distance (part 2): %s', distance2)

    answer1 = reduce(
        operator.mul, [get_num_winning_strategies(t, d) for t, d in zip(times, distances)]
    )

    answer2 = get_num_winning_strategies(time2, distance2)

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
