# coding: utf-8
import argparse
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO, colors
from aocutils.grids import LineGrid

log = getLogger()


UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)

S_REPLACEMENT = {
    (UP, UP): '|',
    (DOWN, DOWN): '|',
    (LEFT, LEFT): '-',
    (RIGHT, RIGHT): '-',
    (UP, RIGHT): 'F',
    (LEFT, DOWN): 'F',
    (RIGHT, DOWN): '7',
    (UP, LEFT): '7',
    (DOWN, LEFT): 'J',
    (RIGHT, UP): 'J',
    (LEFT, UP): 'L',
    (DOWN, RIGHT): 'L',
}

VALID_MOVES = {
    # from_ch -> (to_ch, direction)
    'S': {
        ('|', 'u'),
        ('|', 'd'),
        ('-', 'l'),
        ('-', 'r'),
        ('L', 'd'),
        ('L', 'l'),
        ('J', 'd'),
        ('J', 'r'),
        ('7', 'r'),
        ('7', 'u'),
        ('F', 'u'),
        ('F', 'l'),
    },

    '|': {
        ('|', 'u'),
        ('|', 'd'),
        ('L', 'd'),
        ('J', 'd'),
        ('7', 'u'),
        ('F', 'u'),
        ('S', 'u'),
        ('S', 'd'),
    },

    '-': {
        ('-', 'l'),
        ('-', 'r'),
        ('L', 'l'),
        ('J', 'r'),
        ('7', 'r'),
        ('F', 'l'),
        ('S', 'l'),
        ('S', 'r'),
    },

    'L': {
        ('|', 'u'),
        ('-', 'r'),
        ('J', 'r'),
        ('7', 'r'),
        ('7', 'u'),
        ('F', 'u'),
        ('S', 'u'),
        ('S', 'r'),
    },

    'J': {
        ('|', 'u'),
        ('-', 'l'),
        ('L', 'l'),
        ('7', 'u'),
        ('F', 'u'),
        ('F', 'l'),
        ('S', 'u'),
        ('S', 'l'),
    },

    '7': {
        ('|', 'd'),
        ('-', 'l'),
        ('L', 'l'),
        ('L', 'd'),
        ('J', 'd'),
        ('F', 'l'),
        ('S', 'l'),
        ('S', 'd'),
    },

    'F': {
        ('|', 'd'),
        ('-', 'r'),
        ('L', 'd'),
        ('J', 'd'),
        ('J', 'r'),
        ('7', 'r'),
        ('S', 'r'),
        ('S', 'd'),
    },
}


class Grid(LineGrid):
    def get_loop(self) -> tuple[int, list[tuple[int, int]]]:
        start_r, start_c = self.find('S')
        assert start_r != -1
        assert start_c != -1

        r, c = start_r, start_c
        steps = 0
        visited = {(r, c)}
        path = [(r, c)]
        while True:
            steps += 1
            cur_ch = self.g[r][c]
            for adj_r, adj_c, adj_ch, direction in self.adjacent(r, c):
                move = (adj_ch, direction)
                if move not in VALID_MOVES[cur_ch]:
                    continue

                if (adj_r, adj_c) not in visited or (adj_ch == 'S' and steps > 3):
                    r, c = adj_r, adj_c
                    visited.add((r, c))
                    path.append((r, c))
                    break

            if (r, c) == (start_r, start_c):
                break

        return steps, path

    def render_with_loop_and_inside_cells(self, path, inside_cells) -> str:
        p = set(path)
        i = set(inside_cells)

        def _mark(r, c, ch):
            if (r, c) in p:
                return colors.OKGREEN + ch + colors.ENDC
            if (r, c) in i:
                return colors.RED + ch + colors.ENDC
            return ch

        return "\n".join([
            "".join([_mark(r, c, ch) for c, ch in enumerate(row)])
            for r, row in enumerate(self.g)
        ])

    def scan_inside_cells(self, path) -> int:
        new = self.from_linegrid(self)
        # replace 'S' with an appropriate character to maintain path
        rp, cp = path[-2]  # last element == first element of the path, so we need -2
        rs, cs = path[0]
        rn, cn = path[1]
        dr1, dc1 = rs - rp, cs - cp
        dr2, dc2 = rn - rs, cn - cs
        s_replacement = S_REPLACEMENT[(dr1, dc1), (dr2, dc2)]

        log.debug('S will be replaced with: %s', s_replacement)
        new.g[rs][cs] = s_replacement

        # scan from top to bottom and count inside cells
        inside_cells = set()
        path_items = set(path)
        for r in range(new.rows):
            # flipping is_inside:
            # - if we meet | on path
            # - if we meet L then 7 on path
            # - if we meet F then J on path
            # if is_inside and not is_on_path: mark cell as being inside the loop
            is_inside = False
            entry_ch = None
            exit_ch = None

            for c in range(new.cols):
                cell = (r, c)
                ch = new.g[r][c]
                is_on_path = cell in path_items

                if is_on_path:
                    if ch == '|':
                        is_inside = not is_inside
                    elif ch in {'L', '7', 'F', 'J'}:
                        if entry_ch is None:
                            entry_ch = ch
                        else:
                            exit_ch = ch

                        if entry_ch and exit_ch:
                            if (entry_ch, exit_ch) in {('L', '7'), ('F', 'J')}:
                                is_inside = not is_inside
                            entry_ch, exit_ch = None, None

                if is_inside and not is_on_path:
                    inside_cells.add(cell)

        log.debug(f'Marked:\n{new.render_with_loop_and_inside_cells(path, inside_cells)}\n\n')
        return len(inside_cells)


def main(input_file_name):
    with open(input_file_name) as f:
        lines = [l.strip() for l in f]

    g = Grid.from_lines(lines)
    loop_length, path = g.get_loop()
    log.debug(f'Loop length: {loop_length}, path: {path}')

    assert loop_length % 1 == 0.0
    answer1 = loop_length // 2
    answer2 = g.scan_inside_cells(path)

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
