# coding: utf-8
import argparse
from collections import defaultdict
from dataclasses import dataclass, field
from logging import getLogger
from typing import Optional

import tqdm

from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


WIND_CACHE = {}


@dataclass
class Wind:
    w: defaultdict[list] = field(default_factory=lambda: defaultdict(list))
    rows: int = 0
    cols: int = 0
    _hash: Optional[int] = None

    def __contains__(self, pos):
        return pos in self.w

    @classmethod
    def parse(cls, content):
        w = defaultdict(list)

        lines = content.split('\n')
        rows = len(lines)
        cols = len(lines[0])

        for row_idx, row in enumerate(lines):
            for col_idx, c in enumerate(row):
                if c in {'>', '<', 'v', '^'}:
                    w[(row_idx, col_idx)].append(c)

        return cls(w, rows, cols)

    def occupied_cells(self):
        return set(self.w.keys())

    def step(self):
        cache_key = self
        if cache_key not in WIND_CACHE:
            new = defaultdict(list)
            for (row_idx, col_idx), directions in self.w.items():
                for direction in directions:
                    new_row_idx, new_col_idx = row_idx, col_idx
                    match direction:
                        case '>':
                            wraps = col_idx == self.cols - 2
                            new_col_idx = (col_idx + 1) % (self.cols - 1) + int(wraps)
                        case '<':
                            wraps = col_idx == 1
                            new_col_idx = (col_idx - 1) + (self.cols - 2) * int(wraps)
                        case '^':
                            wraps = row_idx == 1
                            new_row_idx = (row_idx - 1) + (self.rows - 2) * int(wraps)
                        case 'v':
                            wraps = row_idx == self.rows - 2
                            new_row_idx = (row_idx + 1) % (self.rows - 1) + int(wraps)

                    new[(new_row_idx, new_col_idx)].append(direction)

            WIND_CACHE[cache_key] = Wind(new, self.rows, self.cols)
        return WIND_CACHE[cache_key]

    def __hash__(self):
        # Ignore rows & cols since they are the same for the same input
        if self._hash is None:
            thing_to_hash = []
            for key, items in self.w.items():
                thing_to_hash.append(key)
                thing_to_hash.append(tuple(sorted(items)))

            self._hash = hash(tuple(thing_to_hash))
        return self._hash


@dataclass
class Valley:
    v: set[tuple] = field(default_factory=set)
    rows: int = 0
    cols: int = 0
    start: tuple = (0, 0)
    finish: tuple = (0, 0)

    @classmethod
    def parse(cls, content):
        lines = content.split('\n')
        rows = len(lines)
        cols = len(lines[0])
        start = (0, 1)
        finish = (rows - 1, cols - 2)

        v = set()
        for row_idx, row in enumerate(lines):
            for col_idx, c in enumerate(row):
                if c == '#':
                    v.add((row_idx, col_idx))

        return cls(v, rows, cols, start, finish)

    def render(self, wind, player_pos):
        res = []
        for row_idx in range(self.rows):
            row = []
            for col_idx in range(self.cols):
                pos = (row_idx, col_idx)
                if pos in self.v:
                    row.append('#')
                elif pos == player_pos:
                    row.append('E')
                elif pos in wind.w:
                    w = wind.w[pos]
                    if len(w) == 1:
                        row.append(w[0])
                    else:
                        row.append(str(len(w)))
                else:
                    row.append('.')
            res.append(''.join(row))
        return "\n".join(res)

    def valid_moves(self, next_step_wind, player_pos, start, finish):
        ns_occupied_cells = next_step_wind.occupied_cells() | self.v
        ridx, cidx = player_pos

        res = [(ridx, cidx)]

        # edge case - entrance
        if player_pos == start:
            new = (ridx + 1, cidx) if start[0] == 0 else (ridx - 1, cidx)
            res.append(new)

        # edge case - exit
        if (ridx + 1, cidx) == finish or (ridx - 1, cidx) == finish:
            res.append(finish)

        if ridx > 1:
            res.append((ridx - 1, cidx))

        if cidx > 1:
            res.append((ridx, cidx - 1))

        if ridx + 1 < self.rows - 1:
            res.append((ridx + 1, cidx))

        if cidx + 1 < self.cols:
            res.append((ridx, cidx + 1))

        valid_moves = [it for it in res if it not in ns_occupied_cells]

        return valid_moves


def expedition(valley, wind, start, finish, initial_step=0):
    # BFS
    queue = {start}  # set will dedup possible moves
    step = initial_step

    for _ in tqdm.tqdm(range(initial_step)):
        wind = wind.step()

    log.info(
        f'Going from {start} to {finish}, starting at step {step}. Starting grid:\n'
        f'{valley.render(wind, start)}\n'
    )

    progress = tqdm.tqdm()
    while queue:
        progress.update(1)
        step += 1
        new_queue = set()
        wind = wind.step()

        for pos in queue:
            for pos_new in valley.valid_moves(wind, pos, start, finish):
                if pos_new == finish:
                    return step

                new_queue.add(pos_new)
        queue = new_queue

    log.warning(f'Queue is empty:\n{valley.render(wind, pos)}')


def main(input_file_name):
    with open(input_file_name) as f:
        content = f.read().strip()
        wind = Wind.parse(content)
        valley = Valley.parse(content)

    answer1 = expedition(valley, wind, valley.start, valley.finish, 0)
    return_step = expedition(valley, wind, valley.finish, valley.start, answer1)
    answer2 = expedition(valley, wind, valley.start, valley.finish, return_step)

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
