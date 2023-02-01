# coding: utf-8
import argparse
import itertools
import re
from collections import deque
from logging import getLogger
from dataclasses import dataclass, field
from pprint import pformat
import tqdm
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


@dataclass
class V:
    n: str
    rate: int = 0
    tun: list[str] = field(default_factory=list)


def compute_paths(valves):
    # (from node, to node) -> min route length
    paths = {}

    vn_to_open = {'AA'} | {v.n for v in valves.values() if v.rate}
    for vn_from, vn_to in itertools.product(vn_to_open, vn_to_open):
        if vn_from != vn_to:
            paths[(vn_from, vn_to)] = 9999

    for start_vn in vn_to_open:
        for end_vn in vn_to_open:
            if start_vn == end_vn:
                continue

            cur = valves[start_vn]
            path = {cur.n}
            queue = deque([(cur, path)])

            while queue:
                cur, path = queue.popleft()

                if cur.n == end_vn:
                    paths[start_vn, end_vn] = min(paths[start_vn, end_vn], len(path)-1)

                for tn in cur.tun:
                    if tn not in path:
                        queue.append((valves[tn], path | {tn}))
    return paths


def find_max_pressure_released(valves, paths, part=1):
    minutes_limit = 30 if part == 1 else 26
    vn_to_open = {v.n for v in valves.values() if v.rate}

    # path -> max pressure released
    pr_paths = {}

    cur = valves['AA']
    path = {cur.n}

    state = (cur, path, minutes_limit, 0)
    queue = deque([state])

    while queue:
        cur, path, minutes_left, pressure_released = queue.popleft()

        if minutes_left <= 0:
            continue

        for new_vn in vn_to_open:
            if new_vn in path:
                continue

            new_minutes_left = minutes_left - paths[cur.n, new_vn] - 1
            new_pressure_released = pressure_released + valves[new_vn].rate * new_minutes_left
            new_path = path | {new_vn}

            path_key = frozenset(new_path - {'AA'})  # need to exclude AA for part 2 comparison
            if new_pressure_released < pr_paths.get(path_key, 0):
                # trim search space
                continue

            pr_paths[path_key] = new_pressure_released
            queue.append((valves[new_vn], new_path, new_minutes_left, new_pressure_released))

    log.debug('Max pressure released by paths: \n%s', pformat(pr_paths))
    if part == 1:
        return max(pr_paths.values())

    # part 2
    answer2 = 0
    for visited1, visited2 in tqdm.tqdm(itertools.combinations(pr_paths.keys(), 2)):
        # no common elements => path combination can be visited by player & elephant
        if not (visited1 & visited2):
            answer2 = max(answer2, pr_paths[visited1] + pr_paths[visited2])

    return answer2


def main(input_file_name):
    with open(input_file_name) as f:
        lines = f.read().splitlines()

    valves = {}
    line_re = re.compile(r'^Valve (..) .+? rate=(\d+); .+? valves? (.+)$')
    for line in lines:
        m = line_re.match(line)
        name, rate, tunnels = m.groups()
        tunnels = tunnels.split(', ')
        valves[name] = V(name, int(rate), tunnels)

    log.debug('Valves: \n%s', pformat(valves))

    paths = compute_paths(valves)
    log.info('Paths computed')
    answer1 = find_max_pressure_released(valves, paths, 1)
    log.info('Part 1 computed')
    answer2 = find_max_pressure_released(valves, paths, 2)
    log.info('Part 2 computed')

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
