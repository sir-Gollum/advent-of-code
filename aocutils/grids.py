# coding: utf-8
from typing import List, Tuple, Any
from copy import deepcopy

class LineGrid:
    @classmethod
    def from_lines(cls, lines, element_op=str):
        new = cls()
        g = [
            [element_op(ch) for ch in line.strip()]
            for line in lines
        ]
        new.g = g
        new.rows = len(g)
        new.cols = len(g[0])
        return new

    @classmethod
    def from_linegrid(cls, grid):
        new = cls()
        new.g = deepcopy(grid.g)
        new.rows = grid.rows
        new.cols = grid.cols
        return new

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
