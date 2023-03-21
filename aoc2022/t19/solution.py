# coding: utf-8
import argparse
import collections
import math
import re
from dataclasses import dataclass, replace, field
from functools import reduce
from logging import getLogger
from operator import mul
from pprint import pformat
from typing import Tuple, List

import tqdm

from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


@dataclass
class Blueprint:
    blueprint_id: int
    ore_robot_ore_cost: int
    clay_robot_ore_cost: int
    obsidian_robot_ore_cost: int
    obsidian_robot_clay_cost: int
    geode_robot_ore_cost: int
    geode_robot_obsidian_cost: int

    max_ore_cost: int = field(init=False)

    def __post_init__(self):
        self.max_ore_cost = max([
            self.ore_robot_ore_cost,
            self.clay_robot_ore_cost,
            self.obsidian_robot_ore_cost,
            self.geode_robot_ore_cost
        ])


@dataclass
class State:
    r_ore: int = 1
    r_clay: int = 0
    r_obsidian: int = 0
    r_geode: int = 0
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0
    minute: int = 0

    @staticmethod
    def get_time_to_build(res_erq: List[Tuple[int, int, int]]):
        """Resource requirements format: [(cost, current_amount_of_resource, resource_robots)]"""
        if all(cost <= cur for cost, cur, robots in res_erq):
            # already enough resources
            return 1

        # can build when we mine enough of the last resource needed
        return max([
            math.ceil((cost - cur) / robots) + 1
            for cost, cur, robots in res_erq
        ])

    def do_nothing(self):
        new = replace(self)
        new.minute += 1
        new.ore += new.r_ore
        new.clay += new.r_clay
        new.obsidian += new.r_obsidian
        new.geode += new.r_geode
        return new

    def build_next_ore_robot(self, blueprint, minutes_limit):
        min_left = minutes_limit - self.minute
        # no need to build them anymore
        if self.r_ore * min_left + self.ore > blueprint.max_ore_cost * min_left:
            return

        rr = [(blueprint.ore_robot_ore_cost, self.ore, self.r_ore)]
        time_to_build = self.get_time_to_build(rr)
        if self.minute + time_to_build > minutes_limit:
            return

        new = replace(self)
        new.minute += time_to_build
        new.ore = new.ore - blueprint.ore_robot_ore_cost + self.r_ore * time_to_build
        new.clay += new.r_clay * time_to_build
        new.obsidian += new.r_obsidian * time_to_build
        new.geode += new.r_geode * time_to_build
        new.r_ore += 1

        return new

    def build_next_clay_robot(self, blueprint, minutes_limit):
        min_left = minutes_limit - self.minute
        # no need to build them anymore
        if self.r_clay * min_left + self.clay > blueprint.obsidian_robot_clay_cost * min_left:
            return

        rr = [(blueprint.clay_robot_ore_cost, self.ore, self.r_ore)]
        time_to_build = self.get_time_to_build(rr)
        if self.minute + time_to_build > minutes_limit:
            return

        new = replace(self)
        new.minute += time_to_build
        new.ore = new.ore - blueprint.clay_robot_ore_cost + self.r_ore * time_to_build
        new.clay += new.r_clay * time_to_build
        new.obsidian += new.r_obsidian * time_to_build
        new.geode += new.r_geode * time_to_build
        new.r_clay += 1
        return new

    def build_next_obsidian_robot(self, blueprint, minutes_limit):
        min_left = minutes_limit - self.minute
        # no need to build them anymore
        if self.r_clay == 0 or (
            self.r_obsidian * min_left + self.obsidian >
            blueprint.geode_robot_obsidian_cost * min_left
        ):
            return

        rr = [
            (blueprint.obsidian_robot_ore_cost, self.ore, self.r_ore),
            (blueprint.obsidian_robot_clay_cost, self.clay, self.r_clay),
        ]
        time_to_build = self.get_time_to_build(rr)
        if self.minute + time_to_build > minutes_limit:
            return

        new = replace(self)
        new.minute += time_to_build
        new.ore = new.ore - blueprint.obsidian_robot_ore_cost + self.r_ore * time_to_build
        new.clay = new.clay - blueprint.obsidian_robot_clay_cost + self.r_clay * time_to_build
        new.obsidian += new.r_obsidian * time_to_build
        new.geode += new.r_geode * time_to_build
        new.r_obsidian += 1
        return new

    def build_next_geode_robot(self, blueprint, minutes_limit):
        if self.r_obsidian == 0:
            return

        rr = [
            (blueprint.geode_robot_ore_cost, self.ore, self.r_ore),
            (blueprint.geode_robot_obsidian_cost, self.obsidian, self.r_obsidian),
        ]
        time_to_build = self.get_time_to_build(rr)
        if self.minute + time_to_build > minutes_limit:
            return

        new = replace(self)
        new.minute += time_to_build
        new.ore = new.ore - blueprint.geode_robot_ore_cost + self.r_ore * time_to_build
        new.obsidian = (
            new.obsidian - blueprint.geode_robot_obsidian_cost + self.r_obsidian * time_to_build
        )
        new.clay += new.r_clay * time_to_build
        new.geode += new.r_geode * time_to_build
        new.r_geode += 1
        return new


def compute_max_possible_geodes(blueprint: Blueprint, minutes_limit=24):
    log.debug(f'=== Computing blueprint: \n{pformat(blueprint)}')
    state = State()
    queue = collections.deque([(state, [state])])

    max_geodes, max_geodes_history = 0, []
    progress = tqdm.tqdm(desc='Qsize: 1')
    best = {}

    while queue:
        state, history = queue.pop()

        progress.update(1)
        if progress.n % 100000 == 0:
            progress.set_description(f'Qsize: {len(queue)}')

        if state.geode:
            best[state.minute] = max(state.geode, best.get(state.minute, 0))

        # heuristic: keep track of the max number of geodes at this minute.
        # if we are "significantly worse" in the current stagte, abort the branch.
        # "significantly worse" is defined by the magic number and is tunes until it's right :)
        # (higher number == fewer branches aborted and more confidence in the answer)
        # we could make it a formula, but that would complicate things further
        if state.geode < best.get(state.minute, 0) - 4:
            continue

        if state.minute == minutes_limit:
            if state.geode > max_geodes:
                max_geodes = state.geode
                max_geodes_history = history
            continue

        if state.minute == minutes_limit - 1:
            # no point in building robots
            new = state.do_nothing()
            queue.append((new, history + [new]))
            continue

        branched = False
        if new := state.build_next_ore_robot(blueprint, minutes_limit):
            queue.append((new, history + [new]))
            branched = True

        if new := state.build_next_clay_robot(blueprint, minutes_limit):
            queue.append((new, history + [new]))
            branched = True

        if new := state.build_next_obsidian_robot(blueprint, minutes_limit):
            queue.append((new, history + [new]))
            branched = True

        if new := state.build_next_geode_robot(blueprint, minutes_limit):
            queue.append((new, history + [new]))
            branched = True

        if not branched:
            new = state.do_nothing()
            queue.append((new, history + [new]))

    return max_geodes, max_geodes_history


def main(input_file_name):
    blueprints = []
    with open(input_file_name) as f:
        for line in f:
            blueprints.append(Blueprint(*map(int, re.findall(r'\d+', line))))

    log.debug('Blueprints: %s', pformat(blueprints))

    for bp in blueprints:
        mg, hist = compute_max_possible_geodes(bp)
        log.info(f'Max possible geodes for blueprint {bp.blueprint_id}: {mg}')
        for it in hist:
            log.debug(f'  {it}')
        bp.quality_level = bp.blueprint_id * mg

    log.debug('=== Part 2 ===')
    part2 = []
    for bp in blueprints[:3]:
        mg, hist = compute_max_possible_geodes(bp, 32)
        log.info(f'Max possible geodes for blueprint {bp.blueprint_id}: {mg}')
        part2.append(mg)

    print('Answer 1:', sum(bp.quality_level for bp in blueprints))
    print('Answer 2:', reduce(mul, part2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
