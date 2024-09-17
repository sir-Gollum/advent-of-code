# coding: utf-8
from typing import List, Tuple, Any
from copy import deepcopy


class LineGrid:

    def __init__(self, g, rows, cols):
        self.g = g
        self.rows = rows
        self.cols = cols

    @classmethod
    def from_lines(cls, lines, element_op=str, strip_lines=True):
        g = [
            [element_op(ch) for ch in (line.strip() if strip_lines else line)]
            for line in lines
        ]
        return cls(g, len(g), len(g[0]))

    @classmethod
    def from_linegrid(cls, grid):
        return cls(deepcopy(grid.g), grid.rows, grid.cols)

    def render(self, sep='', element_op=str):
        return "\n".join([
            sep.join([element_op(ch) for ch in row])
            for row in self.g
        ])

    def __str__(self):
        return self.render()

    def __unicode__(self):
        return str(self)

    def __repr__(self):
        return str(self)

    def get_row(self, ridx: int) -> List[Any]:
        return self.g[ridx]

    def get_col(self, cidx: int) -> List[Any]:
        return [row[cidx] for row in self.g]

    def find(self, element: Any) -> Tuple[int, int]:
        for ridx, row in enumerate(self.g):
            for cidx, el in enumerate(row):
                if el == element:
                    return ridx, cidx

        return -1, -1

    def adjacent(self, ridx: int, cidx: int, diag=False) -> List[Tuple[int, int, Any, str]]:
        """Return a list of tuples: (ridx, cidx, value, direction)
        that are adjacent the input."""

        res = []
        
        if ridx > 0:
            res.append((ridx-1, cidx, self.g[ridx-1][cidx], 'u'))
            
        if cidx > 0:
            res.append((ridx, cidx-1, self.g[ridx][cidx-1], 'l'))
        
        if ridx + 1 < self.rows:
            res.append((ridx+1, cidx, self.g[ridx+1][cidx], 'd'))
            
        if cidx + 1 < self.cols:
            res.append((ridx, cidx+1, self.g[ridx][cidx+1], 'r'))

        if diag:
            if ridx > 0 and cidx > 0:
                res.append((ridx - 1, cidx - 1, self.g[ridx - 1][cidx - 1], 'ul'))

            if ridx > 0 and cidx + 1 < self.cols:
                res.append((ridx - 1, cidx + 1, self.g[ridx - 1][cidx + 1], 'ur'))

            if ridx + 1 < self.rows and cidx > 0:
                res.append((ridx + 1, cidx - 1, self.g[ridx + 1][cidx - 1], 'dl'))

            if ridx + 1 < self.rows and cidx + 1 < self.cols:
                res.append((ridx + 1, cidx + 1, self.g[ridx + 1][cidx + 1], 'dr'))

        return res
