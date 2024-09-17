# coding: utf-8
import argparse
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO
from aocutils.grids import LineGrid

log = getLogger()


class CachedGrid(LineGrid):
    def __init__(self, g, rows, cols):
        super().__init__(g, rows, cols)
        self.cached_rows = [self.get_row(r) for r in range(self.rows)]
        self.cached_cols = [self.get_col(c) for c in range(self.cols)]


def count_diff(p: CachedGrid, i1: int, i2: int, delta: int, attr: str = 'rows') -> int:
    """Number of different elements between pairs of rows or columns in the pattern"""
    diff = 0
    opposite_attr = getattr(p, 'cols' if attr == 'rows' else 'rows')
    cached_attr = getattr(p, f'cached_{attr}')

    for d in range(delta):
        for idx in range(opposite_attr):
            diff += int(cached_attr[i1 - d][idx] != cached_attr[i2 + d][idx])

    return diff


def horizontal_simmetry_score(p: CachedGrid, part: int = 1) -> int:
    log.debug(f'Checking pattern (rows: {p.rows}, cols: {p.cols}):\n{p.render()}')
    for offset in range(p.rows - 1):
        ir1, ir2 = offset, offset + 1
        diff = count_diff(p, ir1, ir2, 1, 'rows')

        if (part == 1 and diff == 0) or (part == 2 and diff <= 1):
            delta = min(p.rows - ir2, ir1 + 1)
            log.debug(f'Promising rows from {ir1} to {ir2}. Checking range {delta} around')
            for d in range(1, delta):
                log.debug(
                    f'CMP rows {ir1 - d} vs. {ir2 + d}: '
                    f'{"".join(p.cached_rows[ir1 - d])}, {"".join(p.cached_rows[ir2 + d])}: '
                    f'{p.cached_rows[ir1 - d] == p.cached_rows[ir2 + d]} '
                    f'nonequal: {count_diff(p, ir1, ir2, d, "rows")}'
                )

            nonequal = count_diff(p, ir1, ir2, delta, 'rows')
            if part - nonequal == 1:  # exactly 0 for p1, exactly 1 for p2
                log.debug(f'H simmetry found from {ir1 - delta + 1} to {ir2 + delta - 1}')
                return (ir1 + 1) * 100  # examples count from 1
    return 0


def vertical_simmetry_score(p: CachedGrid, part: int = 1) -> int:
    for offset in range(p.cols - 1):
        ic1, ic2 = offset, offset + 1
        diff = count_diff(p, ic1, ic2, 1, 'cols')

        if (part == 1 and diff == 0) or (part == 2 and diff <= 1):
            delta = min(p.cols - ic2, ic1 + 1)
            log.debug(f'Promising cols from {ic1} to {ic2}. Checking range {delta} around')
            for d in range(1, delta):
                log.debug(
                    f'CMP cols {ic1 - d} vs. {ic2 + d}: '
                    f'{"".join(p.cached_cols[ic1 - d])}, {"".join(p.cached_cols[ic2 + d])}: '
                    f'{p.cached_cols[ic1 - d] == p.cached_cols[ic2 + d]} '
                    f'nonequal: {count_diff(p, ic1, ic2, d, "cols")}'
                )

            nonequal = count_diff(p, ic1, ic2, delta, 'cols')
            if part - nonequal == 1:  # exactly 0 for p1, exactly 1 for p2
                log.debug(f'V simmetry found from {ic1 - delta + 1} to {ic2 + delta - 1}')
                return ic1 + 1  # examples count from 1
    return 0


def main(input_file_name):
    patterns = []
    with open(input_file_name) as f:
        for group in f.read().split('\n\n'):
            g = CachedGrid.from_lines(group.splitlines())
            patterns.append(g)

    answer1 = 0
    answer2 = 0

    for p in patterns:
        answer1 += horizontal_simmetry_score(p)
        log.debug('---')
        answer1 += vertical_simmetry_score(p)
        log.debug('')

    log.debug('==== Part 2 ====')

    for p in patterns:
        answer2 += horizontal_simmetry_score(p, part=2)
        log.debug('---')
        answer2 += vertical_simmetry_score(p, part=2)
        log.debug('')

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
