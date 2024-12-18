# coding: utf-8
import argparse
from logging import getLogger

import tqdm
from icecream import ic

import pygame

from aocutils.debug import configure_logging, DEBUG, INFO
from aocutils.grids import LineGrid

log = getLogger()


def vis(animate, g, row_idx, col_idx):
    if not animate:
        return

    pygame.init()
    border_size = 10
    w, h = 1000, 1200
    cell_size = min(
        (w - 2 * border_size) // g.cols, (h - 2 * border_size - 60) // g.rows
    )
    screen = pygame.display.set_mode((w, h))
    screen.fill((0, 0, 0))

    for r in range(g.rows):
        for c in range(g.cols):
            color = (0, 0, 0)
            if g.g[r][c] == ".":
                color = (255, 255, 255)
            if (r, c) == (row_idx, col_idx):
                color = (255, 0, 0)
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    border_size + c * cell_size,
                    border_size + r * cell_size,
                    cell_size,
                    cell_size,
                ),
            )

    font = pygame.font.Font(None, 36)
    text1 = font.render(f"Pos ({row_idx, col_idx})", True, (255, 255, 255))
    screen.blit(text1, (border_size, h - border_size - 60))

    pygame.display.flip()
    pygame.time.wait(100)


class Grid(LineGrid):
    def walk(self, animate=False) -> tuple[set[tuple[int, int, str]], bool]:
        r, c = self.find("^")
        visited_direction = set()

        def _check_visited_direction(a_r, a_c, a_direction):
            key = (a_r, a_c, a_direction)
            if key in visited_direction:
                ic((a_r, a_c, a_direction), visited_direction)
                return True
            visited_direction.add(key)
            return False

        while True:
            for row_idx in range(r, -1, -1):
                if self.g[row_idx][c] == "#":
                    break
                vis(animate, self, row_idx, c)
                if _check_visited_direction(row_idx, c, "u"):
                    return visited_direction, True
            else:
                break
            r = row_idx + 1

            for col_idx in range(c, self.cols):
                if self.g[r][col_idx] == "#":
                    break
                vis(animate, self, r, col_idx)
                if _check_visited_direction(r, col_idx, "r"):
                    return visited_direction, True
            else:
                break
            c = col_idx - 1

            for row_idx in range(r, self.rows):
                if self.g[row_idx][c] == "#":
                    break
                vis(animate, self, row_idx, c)
                if _check_visited_direction(row_idx, c, "d"):
                    return visited_direction, True
            else:
                break
            r = row_idx - 1

            for col_idx in range(c, -1, -1):
                if self.g[r][col_idx] == "#":
                    break
                vis(animate, self, r, col_idx)
                if _check_visited_direction(r, col_idx, "l"):
                    return visited_direction, True
            else:
                break
            c = col_idx + 1

        return visited_direction, False

    def try_obstacles(self, visited) -> int:
        res = 0
        obstacles_to_try = visited - {self.find("^")}

        last_obst_row, last_obst_col = None, None
        for obst_row, obst_col in tqdm.tqdm(obstacles_to_try):
            if last_obst_row is not None:
                self.g[last_obst_row][last_obst_col] = "."
            self.g[obst_row][obst_col] = "#"

            _, loop_found = self.walk(animate=False)
            res += int(loop_found)

            last_obst_row, last_obst_col = obst_row, obst_col
        return res


def main(input_file_name, animate):
    with open(input_file_name) as f:
        g = Grid.from_lines(f.readlines())

    visited_with_direction, _ = g.walk(animate=animate)
    visited = {(r, c) for r, c, _ in visited_with_direction}
    answer1 = len(visited)

    answer2 = g.try_obstacles(visited)

    print("Answer 1:", answer1)
    print("Answer 2:", answer2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-a", "--animate", action="store_true")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    if not args.debug:
        ic.disable()
    main(args.filename, args.animate)
