# coding: utf-8
import argparse
import pprint
from functools import partial
from dataclasses import dataclass, field
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO
from aocutils.grids import LineGrid
from aocutils.graph import dijkstra, DijkstraState

log = getLogger()


@dataclass(order=True)
class St(DijkstraState):
    direction: str = field(default='r', compare=False)
    steps_in_direction: int = field(default=0, compare=False)

    def __hash__(self):
        return hash(self.coord) + hash(self.direction) + hash(self.steps_in_direction)

    def __eq__(self, other):
        return self.coord == other.coord


def get_next_states(
    grid: LineGrid, min_steps_in_direction: int, max_steps_in_direction: int, state: St
):
    ridx, cidx = state.coord
    res = []
    for new_r, new_c, new_loss, new_direction in grid.adjacent(ridx, cidx):
        new_steps = 1
        if new_direction == grid.opposite_direction(state.direction):
            continue

        if new_direction != state.direction:
            if state.steps_in_direction < min_steps_in_direction:
                continue

        if new_direction == state.direction:
            new_steps = state.steps_in_direction + 1
            if new_steps > max_steps_in_direction:
                new_state = St(
                    prio=state.prio + int(new_loss),
                    coord=(new_r, new_c),
                    cost=int(new_loss),
                    direction=new_direction,
                    steps_in_direction=new_steps,
                )
                log.debug(f'Skip state: {state} -> {new_state}')
                continue

        new_state = St(
            prio=state.prio + int(new_loss),
            coord=(new_r, new_c),
            cost=int(new_loss),
            direction=new_direction,
            steps_in_direction=new_steps,
        )
        res.append((new_state, int(new_loss)))
    return res


def main(input_file_name):
    with open(input_file_name) as f:
        grid = LineGrid.from_lines(f.readlines())

    log.debug('Grid: \n%s\n', grid)

    part1_get_next_states = partial(get_next_states, grid, 0, 3)
    part2_get_next_states = partial(get_next_states, grid, 4, 10)

    start = St(prio=0, coord=(0, 0), direction='r', path=[(0, 0)])
    end = St(prio=0, coord=(grid.rows - 1, grid.cols - 1))
    cost1, path1, losses1 = dijkstra(
        start_costs={start: 0},
        end=end,
        get_next_states=part1_get_next_states,
    )
    print('Answer 1:', cost1)

    cost2, path2, losses2 = dijkstra(
        start_costs={start: 0},
        end=end,
        get_next_states=part2_get_next_states,
    )
    log.debug(f'Losses: \n{pprint.pformat(losses2)}')
    log.debug(f'Path: {path2}')
    log.debug(f'Cost: {cost2}')
    print('Answer 2:', cost2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
