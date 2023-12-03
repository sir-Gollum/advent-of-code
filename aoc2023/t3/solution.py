# coding: utf-8
import argparse
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO
from aocutils.grids import LineGrid

log = getLogger()


class Engine(LineGrid):

    def process_num(self, num: list):
        if not num:
            return 0

        for ridx, cidx, _ in num:
            for ar, ac, ch, _ in self.adjacent(ridx, cidx, diag=True):
                if not ch.isdigit() and ch != '.':
                    return int(''.join(it[2] for it in num))

        return 0

    def get_adjacent_numbers(self, ridx: int, cidx) -> list[int]:
        res = []
        visited = set()
        for ar, ac, ch, _ in self.adjacent(ridx, cidx, diag=True):
            if ch.isdigit() and (ar, ac) not in visited:
                left, right = ac, ac
                while left - 1 >= 0 and self.g[ar][left - 1].isdigit():
                    left -= 1
                    visited.add((ar, left))
                while right + 1 < self.cols and self.g[ar][right + 1].isdigit():
                    right += 1
                    visited.add((ar, right))

                res.append(int(''.join(self.g[ar][left:right + 1])))

        return res


def main(input_file_name):
    answer1, answer2 = 0, 0

    with open(input_file_name) as f:
        e = Engine.from_lines(f.readlines())

    num = []
    for ridx in range(e.rows):
        for cidx in range(e.cols):
            # part 1
            if e.g[ridx][cidx].isdigit():
                num.append((ridx, cidx, e.g[ridx][cidx]))
            else:
                answer1 += e.process_num(num)
                num = []

            # part 2
            if e.g[ridx][cidx] == '*':
                adj_numbers = e.get_adjacent_numbers(ridx, cidx)
                log.debug('adj_numbers: %s', adj_numbers)
                if len(adj_numbers) == 2:
                    answer2 += adj_numbers[0] * adj_numbers[1]

    answer1 += e.process_num(num)

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
