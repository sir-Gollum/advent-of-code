# coding: utf-8
import heapq
from dataclasses import dataclass, field
from typing import Callable, Any, List, Tuple


@dataclass(order=True)
class DijkstraState:
    # used to order the queue, equals to cost from start
    prio: int
    coord: tuple[Any, ...] = field(compare=False)

    # cost of the current step
    cost: int = field(default=0, compare=False)
    path: List[Any] = field(default_factory=list, compare=False)

    def __hash__(self):
        return hash(self.coord)

    def __eq__(self, other):
        return self.coord == other.coord


def dijkstra(
    start_costs: dict[DijkstraState, int],
    end: DijkstraState,
    get_next_states: Callable[[DijkstraState], List[Tuple[DijkstraState, int]]],
    cost_limit: int = 10**10,
) -> Tuple[int, List[Any], dict[DijkstraState, int]]:
    queue = []
    for st in start_costs:
        heapq.heappush(queue, st)
    visited = set()
    costs = start_costs

    while queue:
        current_state = heapq.heappop(queue)

        if current_state in visited:
            continue

        visited.add(current_state)

        if current_state == end:
            return current_state.cost, current_state.path, costs

        for next_state, cost in get_next_states(current_state):
            if next_state in visited:
                continue

            new_cost = current_state.cost + cost
            if new_cost < costs.get(next_state, cost_limit):
                next_state.cost = new_cost
                next_state.path = current_state.path + [next_state.coord]
                costs[next_state] = new_cost
                heapq.heappush(queue, next_state)

    return cost_limit, [], costs
