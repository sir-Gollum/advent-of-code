# coding: utf-8
import argparse
from logging import getLogger
import copy
from aocutils.debug import configure_logging, DEBUG, INFO, colors
from aocutils.grids import LineGrid

log = getLogger()


class Grid(LineGrid):

    def __str__(self):
        def _highlight(el):
            return colors.OKGREEN + el + colors.ENDC if el in {'S', 'E'} else el
        return self.render(element_op=_highlight)

    def find_marker(self, marker='S'):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.g[r][c] == marker:
                    return (r, c)

    def get_elevation(self, ch):
        return ord(ch.replace('S', 'a').replace('E', 'z'))

    def find_shortst_path(self, s_ridx, s_cidx, e_ridx, e_cidx):
        # based on Dijkstra's algorithm (which is conveniently in task 15 in AOC 2021)
        cur_ridx, cur_cidx = s_ridx, s_cidx
        cur = (cur_ridx, cur_cidx)

        paths = {cur: 0}
        visited = set()
        candidates = {}
        num_nodes = self.rows * self.cols

        def _get_path_length(ridx, cidx, can_be_huge=False):
            length = paths.get((ridx, cidx), 10**10)
            return length

        while len(paths) < num_nodes:
            for new_ridx, new_cidx, new_ch, _ in self.adjacent(*cur):
                new = (new_ridx, new_cidx)
                if new in visited:
                    continue
                cur_elev = self.get_elevation(self.g[cur_ridx][cur_cidx])
                other_elev = self.get_elevation(new_ch)
                if other_elev - cur_elev > 1: # can't step there - too steep
                    continue

                cur_path_len = _get_path_length(*cur)
                saved_path_len = _get_path_length(*new, can_be_huge=True)

                new_path_len = min(saved_path_len, cur_path_len + 1)
                paths[new] = new_path_len
                candidates[new] = new_path_len

            visited.add(cur)
            candidates.pop(cur, None)
            if not candidates:
                log.info(
                    'Not all points are accessible: %s / %s were analyzed',
                    len(paths), num_nodes
                )
                break

            cur_ridx, cur_cidx = min(candidates.items(), key=lambda x: x[1])[0]
            cur = (cur_ridx, cur_cidx)
            candidates.pop(cur, None)

        return paths.get((e_ridx, e_cidx))



def main(input_file_name):
    with open(input_file_name) as f:
        g = Grid.from_lines(f.readlines())

    log.debug('Grid: \n%s\n', g)
    s_ridx, s_cidx = g.find_marker('S')
    log.debug('Start is at: (%d, %d)', s_ridx, s_cidx)
    e_ridx, e_cidx = g.find_marker('E')
    log.debug('End is at: (%d, %d)', e_ridx, e_cidx)

    answer1 = g.find_shortst_path(s_ridx, s_cidx, e_ridx, e_cidx)

    # In the input, "b" is only in column 1, so we will analyze only starting points
    # in columns 0-2 that start with "a".
    paths = []
    for r_idx in range(g.rows):
        for c_idx in range(3):
            if g.g[r_idx][c_idx] == 'a':
                paths.append(g.find_shortst_path(r_idx, c_idx, e_ridx, e_cidx))

    answer2 = min([p for p in paths if p])

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
