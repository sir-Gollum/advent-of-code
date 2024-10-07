# coding: utf-8
import argparse
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO
from aocutils.grids import LineGrid
from aocutils.iteration import sliding_window

log = getLogger()


class TiltableGrid(LineGrid):

    def tilt_north(self):
        for ridx in range(self.rows):
            for cidx in range(self.cols):
                if self.g[ridx][cidx] == 'O':
                    for ridx_to in range(ridx - 1, -1, -1):
                        if self.g[ridx_to][cidx] in {'#', 'O'}:
                            self.g[ridx][cidx] = '.'
                            self.g[ridx_to + 1][cidx] = 'O'
                            break
                    else:
                        self.g[ridx][cidx] = '.'
                        self.g[0][cidx] = 'O'

    def tilt_west(self):
        for cidx in range(self.cols):
            for ridx in range(self.rows):
                if self.g[ridx][cidx] == 'O':
                    for cidx_to in range(cidx - 1, -1, -1):
                        if self.g[ridx][cidx_to] in {'#', 'O'}:
                            self.g[ridx][cidx] = '.'
                            self.g[ridx][cidx_to + 1] = 'O'
                            break
                    else:
                        self.g[ridx][cidx] = '.'
                        self.g[ridx][0] = 'O'

    def tilt_south(self):
        for ridx in range(self.rows - 1, -1, -1):
            for cidx in range(self.cols):
                if self.g[ridx][cidx] == 'O':
                    for ridx_to in range(ridx + 1, self.rows):
                        if self.g[ridx_to][cidx] in {'#', 'O'}:
                            self.g[ridx][cidx] = '.'
                            self.g[ridx_to - 1][cidx] = 'O'
                            break
                    else:
                        self.g[ridx][cidx] = '.'
                        self.g[self.rows - 1][cidx] = 'O'

    def tilt_east(self):
        for cidx in range(self.cols - 1, -1, -1):
            for ridx in range(self.rows):
                if self.g[ridx][cidx] == 'O':
                    for cidx_to in range(cidx + 1, self.cols):
                        if self.g[ridx][cidx_to] in {'#', 'O'}:
                            self.g[ridx][cidx] = '.'
                            self.g[ridx][cidx_to - 1] = 'O'
                            break
                    else:
                        self.g[ridx][cidx] = '.'
                        self.g[ridx][self.cols - 1] = 'O'

    def cycle(self):
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

    def total_load(self):
        res = 0
        for ridx in range(self.rows):
            for cidx in range(self.cols):
                if self.g[ridx][cidx] == 'O':
                    res += self.rows - ridx
        return res


def main(input_file_name):
    with open(input_file_name) as f:
        g = TiltableGrid.from_lines(f.readlines())
        g2 = TiltableGrid.from_linegrid(g)

    log.debug(f'{g}\n')
    g.tilt_north()
    log.debug(g)
    answer1 = g.total_load()

    cache = {}
    it = 0
    while it < 1000000000:
        cache_key = g2.render()
        if cache_key in cache:
            cache_value = cache[cache_key]

            if len(cache_value) >= 20:
                cache_value.pop(0)

            cache_value.append(it)

            if len(cache_value) > 10:
                diffs = {b - a for a, b in sliding_window(cache_value[-5:], 2)}
                if len(diffs) == 1:
                    cycle_len = diffs.pop()
                    skip = cycle_len * ((1000000000 - it) // cycle_len)
                    log.debug(
                        f'\nCycle if legnth {cycle_len} detected on iteration {it}: '
                        f'{cache_value[-10:]}. Skipping {skip} cycles to {it + skip}\n'
                    )
                    it += skip
                    continue
        else:
            cache[cache_key] = [it]

        g2.cycle()
        it += 1

    answer2 = g2.total_load()

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
