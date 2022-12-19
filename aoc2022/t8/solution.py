# coding: utf-8
import sys
from functools import reduce
from logging import getLogger
from operator import mul

from aocutils.debug import configure_logging, DEBUG, INFO
from aocutils.grids import LineGrid

log = getLogger()


class Grid(LineGrid):
    def left(self, ridx, cidx):
        for it in self.g[ridx][cidx-1::-1]:
            yield it

    def right(self, ridx, cidx):
        for it in self.g[ridx][cidx+1:]:
            yield it

    def top(self, ridx, cidx):
        yield from (self.g[r][cidx] for r in range(ridx-1, -1, -1))

    def bottom(self, ridx, cidx):
        yield from (self.g[r][cidx] for r in range(ridx+1, self.rows))

    def is_visible(self, ridx, cidx):
        if ridx == 0 or cidx == 0 or ridx == self.rows - 1 or cidx == self.cols - 1:
            return True

        v = self.g[ridx][cidx]

        if (
            all(t < v for t in self.left(ridx, cidx))
            or all(t < v for t in self.right(ridx, cidx))
            or all(t < v for t in self.top(ridx, cidx))
            or all(t < v for t in self.bottom(ridx, cidx))
        ):
            return True

        return False

    def scenic_score(self, ridx, cidx):
        if ridx == 0 or cidx == 0 or ridx == self.rows - 1 or cidx == self.cols - 1:
            return 0

        def _vdist(fn):
            n = 0
            for other in fn(ridx, cidx):
                n += 1
                if other >= v:
                    break
            return n

        v = self.g[ridx][cidx]
        score = reduce(mul, [
            _vdist(self.top),
            _vdist(self.bottom),
            _vdist(self.left),
            _vdist(self.right)
        ])

        log.debug(
            'r=%s, c=%s, score=%s. T:%s=>%s, B:%s=>%s, L:%s=>%s, R:%s=>%s',
            ridx, cidx, score,
            list(self.top(ridx, cidx)), _vdist(self.top),
            list(self.bottom(ridx, cidx)), _vdist(self.bottom),
            list(self.left(ridx, cidx)), _vdist(self.left),
            list(self.right(ridx, cidx)), _vdist(self.right),
        )
        return score


def main(input_file_name):
    g = Grid(open(input_file_name).readlines())

    answer1 = sum([
        int(g.is_visible(r, c))
        for r in range(g.rows)
        for c in range(g.cols)
    ])

    answer2 = max([
        g.scenic_score(r, c)
        for r in range(g.rows)
        for c in range(g.cols)
    ])

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    configure_logging(INFO)
    main(sys.argv[1])
