# coding: utf-8
import argparse
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO
from aocutils.grids import LineGrid

log = getLogger()


class G(LineGrid):

    def count_xmas(self, r, c):
        res = 0
        if self.g[r][c] != 'X':
            return res

        for ridx, cidx, chars, direction in self.adjacent(r, c, diag=True, length=3):
            if chars == 'MAS':
                res += 1

        return res

    def count_mas_in_x(self, r, c):
        if self.g[r][c] != 'A':
            return 0

        adj = {}
        for ridx, cidx, chars, direction in self.adjacent(r, c, diag=True):
            if len(direction) == 1:  # only diag directions
                continue

            adj[direction] = chars

        if len(adj) != 4:
            return 0

        if adj['ul'] + adj['dr'] in {'MS', 'SM'} and adj['ur'] + adj['dl'] in {'MS', 'SM'}:
            return 1

        return 0


def main(input_file_name):
    with open(input_file_name) as f:
        grid = G.from_lines(f.readlines())

    answer1, answer2 = 0, 0
    for r in range(grid.rows):
        for c in range(grid.cols):
            answer1 += grid.count_xmas(r, c)
            answer2 += grid.count_mas_in_x(r, c)

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
