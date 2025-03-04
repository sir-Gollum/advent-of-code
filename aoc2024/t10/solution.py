# coding: utf-8
import argparse
from collections import deque, defaultdict
from logging import getLogger
from icecream import ic
from aocutils.debug import configure_logging, DEBUG, INFO
from aocutils.grids import LineGrid

log = getLogger()


class Grid(LineGrid):

    def find_trails(self):
        trails_found = defaultdict(set)
        queue = deque([(th, [th]) for th in self.find_all(0)])

        while queue:
            (c_ridx, c_cidx), trail = queue.popleft()
            cur = self.g[c_ridx][c_cidx]
            if cur == 9:
                trails_found[trail[0]].add(tuple(trail))
                continue

            for n_ridx, n_cidx, nxt, _ in self.adjacent(c_ridx, c_cidx):
                nxt = int(nxt)

                if nxt == cur + 1:
                    queue.append(((n_ridx, n_cidx), trail + [(n_ridx, n_cidx)]))

        return trails_found


def main(input_file_name):
    with open(input_file_name) as f:
        grid = Grid.from_lines(f.readlines(), element_op=int)

    ic(grid, grid.find_all(0))
    grid_trails = grid.find_trails()

    answer1 = 0
    answer2 = 0
    for th, trails in grid_trails.items():
        tmp = {(tr[0], tr[-1]) for tr in trails}
        answer1 += len(tmp)
        answer2 += len(trails)

    print("Answer 1:", answer1)
    print("Answer 2:", answer2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()
    configure_logging(DEBUG if args.debug else INFO)
    if not args.debug:
        ic.disable()
    main(args.filename)
