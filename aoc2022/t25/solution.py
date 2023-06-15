# coding: utf-8
import argparse
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def dec_to_snafu(dec):
    res = []
    while dec > 0:
        ch = str((dec + 2) % 5 - 2).replace("-1", "-").replace("-2", "=")
        res.insert(0, ch)
        dec = (dec + 2) // 5
    return ''.join(res)


def snafu_to_dec(snafu):
    res = 0
    for n, ch in enumerate(reversed(snafu)):
        if ch.isdigit():
            res += int(ch) * (5 ** n)
        elif ch == '-':
            res -= 5 ** n
        elif ch == '=':
            res -= 2 * 5 ** n
    return res


def main(input_file_name):
    with open(input_file_name) as f:
        snafu = f.read().strip().splitlines()

    dec = [snafu_to_dec(it) for it in snafu]
    answer1 = dec_to_snafu(sum(dec))

    print('Answer 1:', answer1)
    print('Answer 2:', 'Smoothie time!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
