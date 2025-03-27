# coding: utf-8
import argparse
from collections import defaultdict
from logging import getLogger
from icecream import ic
from aocutils.debug import configure_logging, DEBUG, INFO
from aocutils.grids import LineGrid
from aocutils.iteration import sequential_groups_of_numbers

log = getLogger()


class Grid(LineGrid):
    def get_regions(self):
        regions = []
        visited = set()

        while len(visited) < self.cells:
            for r, c, _ in self:
                cell = (r, c)
                if cell not in visited:
                    break
            else:
                break

            region, queue = set(), {cell}
            while queue:
                r, c = queue.pop()
                cell, ch = (r, c), self[r][c]
                # ic(cell, ch, len(queue))

                visited.add(cell)
                region.add(cell)

                for nr, nc, nch, _ in self.adjacent(r, c):
                    if nch == ch and (nr, nc) not in visited and (nr, nc) not in region:
                        queue.add((nr, nc))

            regions.append(sorted(region))

        return regions

    @staticmethod
    def compute_region_parameters(regions):
        result = []

        for reg in regions:
            sreg = set(reg)
            perimeter = 0
            sides = defaultdict(list)

            for r, c in reg:
                for dr, dc, direction in (
                    (-1, 0, "u"),
                    (1, 0, "d"),
                    (0, -1, "l"),
                    (0, 1, "r"),
                ):
                    nr, nc = r + dr, c + dc
                    if (nr, nc) not in sreg:
                        perimeter += 1

                        if direction in ("l", "r"):
                            sides[(direction, c)].append(r)
                        else:
                            sides[(direction, r)].append(c)

            result.append((perimeter, reg, sides))

        return result


def main(input_file_name):
    with open(input_file_name) as f:
        grid = Grid.from_lines(f.readlines())

    ic(grid)
    regions = grid.get_regions()

    answer1 = 0
    answer2 = 0
    for perimeter, reg, sides in grid.compute_region_parameters(regions):
        area = len(reg)
        ch = grid[reg[0][0]][reg[0][1]]
        ic(ch, area, perimeter, len(sides), sides)
        answer1 += area * perimeter

        num_of_sides = 0
        for k, v in sides.items():
            side_groups = sequential_groups_of_numbers(v)
            ic(k, v, side_groups)
            num_of_sides += len(side_groups)

        answer2 += area * num_of_sides

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
