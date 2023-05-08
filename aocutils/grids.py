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

    def adjacent(self, ridx: int, cidx: int) -> List[Tuple[int, int, Any, str]]:
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
        
        return res
