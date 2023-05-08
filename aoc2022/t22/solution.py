# coding: utf-8
import argparse
import re
import os
from dataclasses import dataclass
from time import sleep
from logging import getLogger

from aocutils.debug import configure_logging, DEBUG, INFO, colors
from aocutils.grids import LineGrid

log = getLogger()


@dataclass
class Instr:
    steps: int
    turn: str

    @classmethod
    def parse(cls, line):
        res = []
        for s in re.findall(r'(\d+)([RL]?)', line):
            res.append(cls(int(s[0]), s[1]))
        return res


def animation_frame(grid, instr, r, c, extra=''):
    sleep(.1)
    _ = os.system('clear')
    rg = grid.from_linegrid(grid)
    for ridx in range(rg.rows):
        for cidx in range(rg.cols):
            if ridx == r and cidx == c:
                rg.g[ridx][cidx] = colors.RED + rg.g[ridx][cidx] + colors.ENDC
            elif rg.g[ridx][cidx] in {'>', '<', 'v', '^'}:
                rg.g[ridx][cidx] = colors.BOLD + rg.g[ridx][cidx] + colors.ENDC

    log.debug('%s\n\nRow:%s, Col:%s, %s\n%s', rg.render(), r, c, instr, extra)
    # input('>')


class Board(LineGrid):
    @classmethod
    def parse(cls, lines):
        board_lines = lines.split('\n')
        width = max(len(line) for line in board_lines)
        return cls.from_lines(
            [line.ljust(width) for line in board_lines],
            strip_lines=False
        )

    def _cube_side(self, r, c):
        if self.rows == 12:
            #         ....
            #         .A..
            #         ....
            #         ....
            # ............
            # .B...C...D..
            # ............
            # ............
            #         ........
            #         .E...F..
            #         ........
            #         ........
            size = 4
            if r < size:
                side = 'A'
            elif r < size * 2:
                if c < size:
                    side = 'B'
                elif size <= c < size * 2:
                    side = 'C'
                else:
                    side = 'D'
            else:
                if c < size * 3:
                    side = 'E'
                else:
                    side = 'F'
        else:
            # 200 rows, real input
            #     ........
            #     .A...B..
            #     ........
            #     ........
            #     ....
            #     .C..
            #     ....
            #     ....
            # ........
            # .D...E..
            # ........
            # ........
            # ....
            # .F..
            # ....
            # ....
            size = 50
            if r < size:
                if c < size * 2:
                    side = 'A'
                else:
                    side = 'B'
            elif r < size * 2:
                side = 'C'
            elif size * 2 <= r < size * 3:
                if c < size:
                    side = 'D'
                else:
                    side = 'E'
            else:
                side = 'F'

        return side

    def _topleft(self, side):
        # side name -> (row, col) of top left corner
        if self.rows == 12:
            size = 4
            return {
                'A': (0, size * 2),
                'B': (size, 0),
                'C': (size, size),
                'D': (size, size * 2),
                'E': (size * 2, size * 2),
                'F': (size * 2, size * 3),
            }[side]
        else:
            # real input
            size = 50
            return {
                'A': (0, size),
                'B': (0, size * 2),
                'C': (size, size),
                'D': (size * 2, 0),
                'E': (size * 2, size),
                'F': (size * 3, 0),
            }[side]

    def _next_cell(self, cur_r, cur_c, cur_direction):
        match cur_direction:
            case '>':
                return cur_r, (cur_c + 1) % self.cols, (cur_c + 1) % self.cols != cur_c + 1
            case '<':
                return cur_r, (cur_c - 1) % self.cols, (cur_c - 1) % self.cols != cur_c - 1
            case '^':
                return (cur_r - 1) % self.rows, cur_c, (cur_r - 1) % self.rows != cur_r - 1
            case 'v':
                return (cur_r + 1) % self.rows, cur_c, (cur_r + 1) % self.rows != cur_r + 1

        raise ValueError(f'Invalid direction: "{cur_direction}"')

    def step(self, r, c, direction):
        new_r, new_c, _ = self._next_cell(r, c, direction)
        while self.g[new_r][new_c] == ' ':
            new_r, new_c, _ = self._next_cell(new_r, new_c, direction)

        if self.g[new_r][new_c] == '#':
            return r, c

        return new_r, new_c

    def step_cube(self, r, c, direction):
        new_r, new_c, circled = self._next_cell(r, c, direction)
        side = self._cube_side(r, c)
        new_direction = direction

        while self.g[new_r][new_c] == ' ' or circled:  # circles is edge case for example input
            circled = False
            if self.rows == 12:
                # hard-coded example folding, only need to describe disconnected edges, not folded
                F = 3  # edge size - 1, flips coordinates
                cur_tl_r, cur_tl_c = self._topleft(side)
                match (side, direction):
                    case ('A', '>'):
                        tl_r, tl_c = self._topleft('F')
                        new_direction = '<'
                        new_r, new_c = (tl_r + F - new_r), tl_c + F
                    case ('A', '<'):
                        tl_r, tl_c = self._topleft('C')
                        new_direction = 'v'
                        new_r, new_c = tl_r, (tl_c + new_r)
                    case ('A', '^'):
                        tl_r, tl_c = self._topleft('C')
                        new_direction = 'v'
                        new_r, new_c = tl_r, (tl_c + F - new_c)

                    case ('B', '<'):
                        tl_r, tl_c = self._topleft('F')
                        new_direction = '^'
                        new_r, new_c = tl_r + F, (tl_c + F - (new_r - cur_tl_r))
                    case ('B', '^'):
                        tl_r, tl_c = self._topleft('A')
                        new_direction = 'v'
                        new_r, new_c = 0, (tl_c + F - (new_c - cur_tl_c))
                    case ('B', 'v'):
                        tl_r, tl_c = self._topleft('E')
                        new_direction = '^'
                        new_r, new_c = tl_r + F, (tl_c + F - (new_c - cur_tl_c))

                    case ('C', '^'):
                        tl_r, tl_c = self._topleft('A')
                        new_direction = '>'
                        new_r, new_c = tl_r + (new_c - cur_tl_c), tl_c
                    case ('C', 'v'):
                        tl_r, tl_c = self._topleft('E')
                        new_direction = '>'
                        new_r, new_c = tl_r + (new_c - cur_tl_c), tl_c

                    case ('D', '>'):
                        tl_r, tl_c = self._topleft('F')
                        new_direction = 'v'
                        new_r, new_c = tl_r, tl_c + F - (new_r - cur_tl_r)

                    case ('E', '<'):
                        tl_r, tl_c = self._topleft('C')
                        new_direction = '^'
                        new_r, new_c = tl_r + F, tl_c + F - (new_r - cur_tl_r)
                    case ('E', 'v'):
                        tl_r, tl_c = self._topleft('B')
                        new_direction = '^'
                        new_r, new_c = tl_r + F, tl_c + F - (new_c - cur_tl_c)

                    case ('F', '>'):
                        tl_r, tl_c = self._topleft('A')
                        new_direction = '<'
                        new_r, new_c = tl_r + F - (new_r - cur_tl_r), tl_c + F
                    case ('F', '^'):
                        tl_r, tl_c = self._topleft('D')
                        new_direction = '<'
                        new_r, new_c = tl_r + F - (new_c - cur_tl_c), tl_c + F
                    case ('F', 'v'):
                        tl_r, tl_c = self._topleft('B')
                        new_direction = '>'
                        new_r, new_c = tl_r + F - (new_c - cur_tl_c), tl_c
            else:
                # real input
                # hard-coded folding, only need to describe disconnected edges, not folded edges
                F = 49  # edge size - 1, flips coordinates
                cur_tl_r, cur_tl_c = self._topleft(side)
                match (side, direction):
                    case ('A', '^'):
                        tl_r, tl_c = self._topleft('F')
                        new_direction = '>'
                        new_r, new_c = tl_r + (new_c - cur_tl_c), tl_c
                    case ('A', '<'):
                        tl_r, tl_c = self._topleft('D')
                        new_direction = '>'
                        new_r, new_c = tl_r + F - (new_r - cur_tl_r), tl_c

                    case ('B', '^'):
                        tl_r, tl_c = self._topleft('F')
                        new_direction = '^'
                        new_r, new_c = tl_r + F, tl_c + (new_c - cur_tl_c)
                    case ('B', '>'):
                        tl_r, tl_c = self._topleft('E')
                        new_direction = '<'
                        new_r, new_c = tl_r + F - (new_r - cur_tl_r), tl_c + F
                    case ('B', 'v'):
                        tl_r, tl_c = self._topleft('C')
                        new_direction = '<'
                        new_r, new_c = tl_r + (new_c - cur_tl_c), tl_c + F

                    case ('C', '<'):
                        tl_r, tl_c = self._topleft('D')
                        new_direction = 'v'
                        new_r, new_c = tl_r, tl_c + (new_r - cur_tl_r)
                    case ('C', '>'):
                        tl_r, tl_c = self._topleft('B')
                        new_direction = '^'
                        new_r, new_c = tl_r + F, tl_c + (new_r - cur_tl_r)

                    case ('D', '<'):
                        tl_r, tl_c = self._topleft('A')
                        new_direction = '>'
                        new_r, new_c = tl_r + F - (new_r - cur_tl_r), tl_c
                    case ('D', '^'):
                        tl_r, tl_c = self._topleft('C')
                        new_direction = '>'
                        new_r, new_c = tl_r + (new_c - cur_tl_c), tl_c

                    case ('E', '>'):
                        tl_r, tl_c = self._topleft('B')
                        new_direction = '<'
                        new_r, new_c = tl_r + F - (new_r - cur_tl_r), tl_c + F
                    case ('E', 'v'):
                        tl_r, tl_c = self._topleft('F')
                        new_direction = '<'
                        new_r, new_c = tl_r + (new_c - cur_tl_c), tl_c + F

                    case ('F', '<'):
                        tl_r, tl_c = self._topleft('A')
                        new_direction = 'v'
                        new_r, new_c = tl_r, tl_c + (new_r - cur_tl_r)
                    case ('F', 'v'):
                        tl_r, tl_c = self._topleft('B')
                        new_direction = 'v'
                        new_r, new_c = tl_r, tl_c + (new_c - cur_tl_c)
                    case ('F', '>'):
                        tl_r, tl_c = self._topleft('E')
                        new_direction = '^'
                        new_r, new_c = tl_r + F, tl_c + (new_r - cur_tl_r)

        if self.g[new_r][new_c] == '#':
            return r, c, direction

        return new_r, new_c, new_direction

    def walk(self, instructions, animate=False, is_cube=False, start_pos=None):
        log.debug('Walking instructions: \n%s', instructions)


        if start_pos:
            r, c, direction = start_pos
        else:
            r = 0
            c = self.g[r].index('.')
            direction = '>'
        self.g[r][c] = direction

        for instr in instructions:
            for step in range(instr.steps):
                if is_cube:
                    new_r, new_c, direction = self.step_cube(r, c, direction)
                else:
                    new_r, new_c = self.step(r, c, direction)
                self.g[new_r][new_c] = direction

                if animate and (new_r!= r or new_c!= c):
                    # skip frames if we're at the same place
                    side = self._cube_side(r, c)
                    animation_frame(
                        self, instr, new_r, new_c, f'\nSide: {side}\nStep: {step+1}/{instr.steps}'
                    )

                r, c = new_r, new_c

            if instr.turn:
                direction = {
                    'R': {
                        '>': 'v', 'v': '<', '<': '^', '^': '>'
                    },
                    'L': {
                        '>': '^', '^': '<', '<': 'v', 'v': '>'
                    }
                }[instr.turn][direction]
                self.g[r][c] = direction

            if animate:
                side = self._cube_side(r, c)
                animation_frame(self, instr, r, c, f'\nSide: {side}\nTurned to {instr.turn}')

        log.debug('Final state:\n%s\n\nRow:%s, Col:%s, Dir:%s', self.render(), r, c, direction)
        direction_scores = {'>': 0, 'v': 1, '<': 2, '^': 3}
        return 1000 * (r + 1) + 4 * (c + 1) + direction_scores[direction]


def main(input_file_name, animate=False):
    with open(input_file_name) as f:
        parts = f.read().rstrip().split('\n\n')
        board = Board.parse(parts[0])
        board2 = Board.parse(parts[0])
        instructions = Instr.parse(parts[1])

    answer1 = board.walk(instructions, animate)
    answer2 = board2.walk(instructions, animate, is_cube=True)
    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-a', '--animate', action='store_true')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename, args.animate)
