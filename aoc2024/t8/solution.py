# coding: utf-8
import argparse
import itertools
from logging import getLogger
from icecream import ic
from aocutils.debug import configure_logging, DEBUG, INFO
from aocutils.grids import LineGrid

log = getLogger()


class Grid(LineGrid):
    def get_antinode_coordinates(self) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        antenna_types = set()
        for row in self.g:
            for cell in row:
                if cell != '.':
                    antenna_types.add(cell)

        res_1, res_multi = set(), set()
        for antenna_type in antenna_types:
            antennas = self.find_all(antenna_type)
            for a, b in itertools.permutations(antennas, 2):
                dr = b[0] - a[0]
                dc = b[1] - a[1]

                for it in range(0, 1000):
                    new_r = b[0] + dr * it
                    new_c = b[1] + dc * it

                    if self.is_coord_in_grid(new_r, new_c):
                        res_multi.add((new_r, new_c))
                        if it == 1:
                            res_1.add((new_r, new_c))
        return sorted(res_1), sorted(res_multi)


def main(input_file_name):
    with open(input_file_name) as f:
        g = Grid.from_lines(f.readlines())
    ic(g)

    antenna_coordinates = g.get_antinode_coordinates()
    answer1 = len(antenna_coordinates[0])
    answer2 = len(antenna_coordinates[1])
    ic(antenna_coordinates)

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    configure_logging(DEBUG if args.debug else INFO)
    if not args.debug:
        ic.disable()
    main(args.filename)
