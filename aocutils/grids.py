# coding: utf-8
from typing import Any
from copy import deepcopy

OPPOSITE_DIRECTIONS = {
    "u": "d",
    "d": "u",
    "l": "r",
    "r": "l",
    "ul": "dr",
    "ur": "dl",
    "dl": "ur",
    "dr": "ul",
}


class LineGrid:

    def __init__(self, g, rows, cols):
        self.g = g
        self.rows = rows
        self.cols = cols
        self.cells = rows * cols
        self._iter_state = None

    @classmethod
    def from_lines(cls, lines: list[str], element_op=str, strip_lines=True):
        g = [
            [element_op(ch) for ch in (line.strip() if strip_lines else line)]
            for line in lines
        ]
        return cls(g, len(g), len(g[0]))

    @classmethod
    def from_linegrid(cls, grid: "LineGrid"):
        return cls(deepcopy(grid.g), grid.rows, grid.cols)

    @staticmethod
    def opposite_direction(direction: str) -> str:
        return OPPOSITE_DIRECTIONS[direction]

    def render(self, sep: str = "", element_op=str):
        return "\n".join([sep.join([element_op(ch) for ch in row]) for row in self.g])

    def __str__(self):
        return self.render()

    def __unicode__(self):
        return str(self)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        it = ((r, c) for r in range(self.rows) for c in range(self.cols))
        self._iter_state = it
        return self

    def __next__(self):
        r, c = next(self._iter_state)
        return r, c, self.g[r][c]

    def __getitem__(self, item: int):
        return self.g[item]

    def get_row(self, ridx: int) -> list[Any]:
        return self.g[ridx]

    def get_col(self, cidx: int) -> list[Any]:
        return [row[cidx] for row in self.g]

    def find(self, element: Any) -> tuple[int, int]:
        for ridx, row in enumerate(self.g):
            for cidx, el in enumerate(row):
                if el == element:
                    return ridx, cidx
        return -1, -1

    def find_all(self, element: Any) -> list[tuple[int, int]]:
        res = []
        for ridx, row in enumerate(self.g):
            for cidx, el in enumerate(row):
                if el == element:
                    res.append((ridx, cidx))
        return res

    def adjacent(
        self, ridx: int, cidx: int, diag: bool = False, length: int = 1
    ) -> list[tuple[int, int, str, str]]:
        """Return a list of tuples: (ridx, cidx, value, direction)
        that are adjacent the input."""

        res = []

        directions = [("u", -1, 0), ("d", 1, 0), ("l", 0, -1), ("r", 0, 1)]

        if diag:
            directions.extend(
                [("ul", -1, -1), ("ur", -1, 1), ("dl", 1, -1), ("dr", 1, 1)]
            )

        for direction, dr, dc in directions:
            chars = []
            for i in range(1, length + 1):
                nr, nc = ridx + dr * i, cidx + dc * i
                if self.is_coord_in_grid(nr, nc):
                    chars.append(str(self.g[nr][nc]))
                else:
                    break
            if len(chars) == length:
                res.append((ridx + dr, cidx + dc, "".join(chars), direction))

        return res

    def is_coord_in_grid(self, ridx: int, cidx: int) -> bool:
        return 0 <= ridx < self.rows and 0 <= cidx < self.cols
