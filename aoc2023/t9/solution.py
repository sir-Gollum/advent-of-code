# coding: utf-8
import argparse
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def extrapolate(series: list[int]):
    derivatives = [series[:]]

    while any(it != 0 for it in derivatives[-1]):
        last_derivative = derivatives[-1]
        new = []
        for n, v in enumerate(last_derivative[:-1]):
            new.append(last_derivative[n + 1] - v)
        derivatives.append(new)

    log.debug(f'Deriving series')
    for d in derivatives:
        log.debug(d)

    derivatives[-1].append(0)
    for n in range(len(derivatives) - 2, -1, -1):
        derivatives[n].append(derivatives[n + 1][-1] + derivatives[n][-1])
        derivatives[n].insert(0, derivatives[n][0] - derivatives[n + 1][0])

    return derivatives[0][0], derivatives[0][-1]


def main(input_file_name):
    with open(input_file_name) as f:
        series = [list(map(int, line.strip().split())) for line in f]

    extrapolated = [extrapolate(s) for s in series]
    answer1 = sum(e[1] for e in extrapolated)
    answer2 = sum(e[0] for e in extrapolated)
    log.debug(f'Series: {series}')

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
