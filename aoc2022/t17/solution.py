# coding: utf-8
import argparse
import itertools
import os
import textwrap
from logging import getLogger
from time import sleep

import tqdm

from aocutils.debug import configure_logging, DEBUG, INFO, colors

log = getLogger()

SHAPES = [
    '####',
    """
        .#.
        ###
        .#.
    """,
    """
        ..#
        ..#
        ###
    """,
    """
        #
        #
        #
        #
    """,
    """
        ##
        ##
    """,
]


class Figure:
    def __init__(self, shape):
        self.shape = textwrap.dedent(shape).strip().split('\n')
        self.w = len(self.shape[0])
        self.h = len(self.shape)

        self.deltas = set()
        for row_idx, row in enumerate(self.shape):
            for col_idx, char in enumerate(row):
                if char == '#':
                    self.deltas.add(complex(col_idx, -row_idx))

    def coordinates(self, topleft):
        for it in self.deltas:
            yield topleft + it


def animation_frame(chamber, chamber_height, rock, rock_pos, wind):
    sleep(.1)
    _ = os.system('clear')

    rock_coords = set(rock.coordinates(rock_pos))
    top_buffer = 7  # how many rows on top to draw
    scroll_buffer = 60  # vertical size (+ top buffer) before we start scrolling
    num_pad = 4

    result = []
    for rrow_idx in range(min(scroll_buffer, chamber_height + top_buffer)):
        row_idx = chamber_height - rrow_idx + top_buffer
        row = [str(row_idx).rjust(num_pad), '|']
        for col_idx in range(7):
            c = complex(col_idx, row_idx)
            ch = '.'
            if c in rock_coords:
                ch = colors.RED + '@' + colors.ENDC
            if c in chamber:
                ch = colors.OKGREEN + '#' + colors.ENDC
            row.append(ch)
        row.append('|')
        result.append(''.join(row))

    result.append(' ' * num_pad + '+-------+')
    result.append(f'W: {wind}, H: {chamber_height}')
    return '\n'.join(result)


def simulate(figures, wind, animate, rocks_to_drop):
    figures = itertools.cycle(enumerate(figures))
    wind = itertools.cycle(enumerate(wind))
    gust_deltas = {'>': 1, '<': -1}

    chamber = set()
    chamber_width = 7

    stats = {}
    required_stat_confidence = 10

    rocks_dropped = 0
    height = 0
    progress = tqdm.tqdm(total=rocks_to_drop, disable=animate)
    while rocks_dropped < rocks_to_drop:
        rock_idx, rock = next(figures)
        gust_idx = -1
        pos = complex(2, height + rock.h + 3)
        is_placed = False

        while not is_placed:
            gust_idx, gust = next(wind)
            gust_delta = gust_deltas[gust]
            if animate:
                log.info(animation_frame(chamber, int(height), rock, pos, gust))
                # input()

            for c in rock.coordinates(pos + gust_delta):
                if c in chamber or c.real < 0 or c.real == chamber_width:
                    # can't move to the side
                    break
            else:
                pos += gust_delta

            for c in rock.coordinates(pos - 1j):
                if c in chamber or c.imag == 0:
                    # can't move down
                    is_placed = True
                    for stop_c in rock.coordinates(pos):
                        chamber.add(stop_c)
                    rocks_dropped += 1
                    height = max(height, pos.imag)
                    progress.update(1)
                    stats.setdefault((rock_idx, gust_idx), []).append((height, rocks_dropped))
                    break
            else:
                pos -= 1j

        # if we collected enough stats, we can jump to the end
        stat = stats.get((rock_idx, gust_idx))
        if stat and len(stat) >= required_stat_confidence:
            h_deltas = set()
            rd_deltas = set()
            for i in range(1, len(stat)):
                h_deltas.add(stat[i][0] - stat[i-1][0])
                rd_deltas.add(stat[i][1] - stat[i-1][1])

            if len(h_deltas) == 1 and len(rd_deltas) == 1:
                rocks_dropped_per_skip = int(rd_deltas.pop())
                height_added_per_skip = int(h_deltas.pop())
                if (rocks_to_drop - rocks_dropped) % rocks_dropped_per_skip == 0:
                    skips = int((rocks_to_drop - rocks_dropped) / rocks_dropped_per_skip)
                    log.debug(
                        f'Cycle found: rocks={rocks_dropped_per_skip}, '
                        f'height={height_added_per_skip}. \n'                        
                        f'Skipping from {rocks_dropped} '
                        f'to {rocks_dropped + rocks_dropped_per_skip * skips} rocks '
                        f'({rocks_dropped_per_skip * skips} rocks skipped). '
                        f'Cycles skipped: {int(skips)}, rocks per cycle: {rocks_dropped_per_skip}'
                    )
                    height += height_added_per_skip * skips
                    rocks_dropped += rocks_dropped_per_skip * skips
                    chamber = {c + complex(0, height_added_per_skip * skips) for c in chamber}
                    progress.update(rocks_dropped_per_skip * skips)

    return height


def main(input_file_name, animate=False):
    figures = [Figure(shape) for shape in SHAPES]
    with open(input_file_name) as f:
        wind = f.read().strip()

    answer1 = simulate(figures, wind, animate, 2022)
    answer2 = simulate(figures, wind, animate, 1000000000000)

    print('Answer 1:', int(answer1))
    print('Answer 2:', int(answer2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-a', '--animate', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename, args.animate)
