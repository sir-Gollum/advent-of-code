# coding: utf-8
"""
--- Day 23: Amphipod ---

A group of amphipods notice your fancy submarine and flag you down. "With such an impressive shell," one amphipod says, "surely you can help us with a question that has stumped our best scientists."

They go on to explain that a group of timid, stubborn amphipods live in a nearby burrow. Four types of amphipods live there: Amber (A), Bronze (B), Copper (C), and Desert (D). They live in a burrow that consists of a hallway and four side rooms. The side rooms are initially full of amphipods, and the hallway is initially empty.

They give you a diagram of the situation (your puzzle input), including locations of each amphipod (A, B, C, or D, each of which is occupying an otherwise open space), walls (#), and open space (.).

For example:

#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
The amphipods would like a method to organize every amphipod into side rooms so that each side room contains one type of amphipod and the types are sorted A-D going left to right, like this:

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
Amphipods can move up, down, left, or right so long as they are moving into an unoccupied open space. Each type of amphipod requires a different amount of energy to move one step: Amber amphipods require 1 energy per step, Bronze amphipods require 10 energy, Copper amphipods require 100, and Desert ones require 1000. The amphipods would like you to find a way to organize the amphipods that requires the least total energy.

However, because they are timid and stubborn, the amphipods have some extra rules:

Amphipods will never stop on the space immediately outside any room. They can move into that space so long as they immediately continue moving. (Specifically, this refers to the four open spaces in the hallway that are directly above an amphipod starting position.)
Amphipods will never move from the hallway into a room unless that room is their destination room and that room contains no amphipods which do not also have that room as their own destination. If an amphipod's starting room is not its destination room, it can stay in that room until it leaves the room. (For example, an Amber amphipod will not move from the hallway into the right three rooms, and will only move into the leftmost room if that room is empty or if it only contains other Amber amphipods.)
Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room. (That is, once any amphipod starts moving, any other amphipods currently in the hallway are locked in place and will not move again until they can move fully into a room.)
In the above example, the amphipods can be organized using a minimum of 12521 energy. One way to do this is shown below.

Starting configuration:

#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
One Bronze amphipod moves into the hallway, taking 4 steps and using 40 energy:

#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########
The only Copper amphipod not in its side room moves there, taking 4 steps and using 400 energy:

#############
#...B.......#
###B#.#C#D###
  #A#D#C#A#
  #########
A Desert amphipod moves out of the way, taking 3 steps and using 3000 energy, and then the Bronze amphipod takes its place, taking 3 steps and using 30 energy:

#############
#.....D.....#
###B#.#C#D###
  #A#B#C#A#
  #########
The leftmost Bronze amphipod moves to its room using 40 energy:

#############
#.....D.....#
###.#B#C#D###
  #A#B#C#A#
  #########
Both amphipods in the rightmost room move into the hallway, using 2003 energy in total:

#############
#.....D.D.A.#
###.#B#C#.###
  #A#B#C#.#
  #########
Both Desert amphipods move into the rightmost room using 7000 energy:

#############
#.........A.#
###.#B#C#D###
  #A#B#C#D#
  #########
Finally, the last Amber amphipod moves into its room, using 8 energy:

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
What is the least energy required to organize the amphipods?

Your puzzle answer was 13556.

--- Part Two ---

As you prepare to give the amphipods your solution, you notice that the diagram they handed you was actually folded up. As you unfold it, you discover an extra part of the diagram.

Between the first and second lines of text that contain amphipod starting positions, insert the following lines:

  #D#C#B#A#
  #D#B#A#C#
So, the above example now becomes:

#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########
The amphipods still want to be organized into rooms similar to before:

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
In this updated example, the least energy required to organize these amphipods is 44169:

#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#..........D#
###B#C#B#.###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A.........D#
###B#C#B#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A........BD#
###B#C#.#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A......B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#.#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#C#.#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA...B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#D#C#A#
  #########

#############
#AA.D.B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#.#C#A#
  #########

#############
#AA.D...B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#B#C#A#
  #########

#############
#AA.D.....BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#.#.###
  #D#B#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#A#
  #########

#############
#AA.D.....AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#.#
  #########

#############
#AA.......AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #.#B#C#.#
  #D#B#C#D#
  #A#B#C#D#
  #########

#############
#AA.D.....AD#
###.#B#C#.###
  #.#B#C#.#
  #.#B#C#D#
  #A#B#C#D#
  #########

#############
#A..D.....AD#
###.#B#C#.###
  #.#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...D.....AD#
###.#B#C#.###
  #A#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#.........AD#
###.#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#..........D#
###A#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
Using the initial configuration from the full diagram, what is the least energy required to organize the amphipods?

Your puzzle answer was 54200.
"""


import sys
from dataclasses import dataclass
import typing as tp


cache = {}

# Rooms consist of multiple slots
# Each room is for its own kind of creatures

# room index -> entrance index in the hallway
RINDEX = (2, 4, 6, 8)
DEST_ROOMS = ['A', 'B', 'C', 'D']
MOVE_COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
PATH_BLOCK = {'A', 'B', 'C', 'D'}


@dataclass
class B:
    b: tuple[tuple[str]]

    def __hash__(self):
        return hash(self.b)

    @classmethod
    def from_iter(cls, hall: str, *rooms):
        hall = list(hall)
        for idx in RINDEX:
            hall[idx] = 'X'

        b = [tuple(hall)]
        for r in rooms:
            b.append(tuple(r))
        return cls(tuple(b))

    @classmethod
    def from_input(cls, data: str):
        b = []
        lines = [l.strip() for l in data.splitlines()]

        hall = list(lines[1][1:-1])
        for idx in RINDEX:
            hall[idx] = 'X'
        b.append(tuple(hall))

        rooms = [[] for _ in RINDEX]

        for room_line in lines[2:-1]:
            for r_idx, r_ch in enumerate(room_line.replace('#', ' ').split()):
                rooms[r_idx].append(r_ch)

        for room in rooms:
            b.append(tuple(room))

        return cls(tuple(b))

    @property
    def hall(self):
        return self.b[0]

    @property
    def rooms(self):
        return self.b[1:]

    @property
    def room_len(self):
        return len(self.b[1])

    @property
    def hall_len(self):
        return len(self.b[0])

    def vis(self):
        res = []
        total = len(self.b[0]) + 2
        res.append('#' * total)
        res.append('#' + ''.join(self.b[0]) + '#')

        for slot_idx in range(self.room_len):
            line = [' ' for _ in range(total)]
            for room_idx, room in enumerate(self.rooms):
                line[RINDEX[room_idx]+1] = room[slot_idx]

            res.append(
                (''.join(line))
            )
        return '\n'.join(res)

    def is_solved(self):
        for room, ch in zip(self.rooms, DEST_ROOMS):
            if set(room) != set(ch):
                return False
        return True

    def after_move(self, arr_idx_start: int, slot_idx_start: int, arr_idx_end: int, slot_idx_end: int):
        new_b = [list(it) for it in self.b]
        try:
            assert new_b[arr_idx_end][slot_idx_end] == '.'
        except IndexError:
            print(f'Invalid move: ({arr_idx_start}, {slot_idx_start}) -> ({arr_idx_end}, {slot_idx_end})')
            raise

        new_b[arr_idx_end][slot_idx_end] = new_b[arr_idx_start][slot_idx_start]
        new_b[arr_idx_start][slot_idx_start] = '.'
        return B.from_iter(*new_b)

    def path(
            self, arr_idx_start: int, slot_idx_start: int, arr_idx_end: int, slot_idx_end: int
    ) -> str:
        """Construct path between 2 points"""
        p = []
        if arr_idx_start:
            # In a room, going to the hall
            p += reversed(self.b[arr_idx_start][:slot_idx_start])
            src_room_idx = RINDEX[arr_idx_start - 1]  # turning point in the hall
            if not arr_idx_end:
                # target is in the hall
                target_hall_idx = slot_idx_end
            else:
                # target is in another room
                target_hall_idx = RINDEX[arr_idx_end - 1] # second turning point in the hall

            # path in the hall
            if target_hall_idx < src_room_idx:
                # left from the room
                p += reversed(self.b[0][target_hall_idx: src_room_idx + 1])
            else:
                p += self.b[0][src_room_idx: target_hall_idx + 1]

            if arr_idx_end:
                # target is another room
                p += self.b[arr_idx_end][:slot_idx_end + 1]
        else:
            # in a hall
            room_idx = RINDEX[arr_idx_end - 1]  # turning point in the hall
            if slot_idx_start < room_idx:
                p += self.b[0][slot_idx_start+1: room_idx + 1]
            else:
                p += reversed(self.b[0][room_idx: slot_idx_start])

            # path in the room
            p += self.b[arr_idx_end][:slot_idx_end + 1]
        assert p
        return ''.join(p)

    def char_positions(self) -> tp.Iterator[tuple[int, int]]:
        for array_idx, array in enumerate(self.b):
            for slot, ch in enumerate(array):
                if ch in PATH_BLOCK:
                    yield array_idx, slot

    def is_valid_path(self, p: str) -> bool:
        if not p.endswith('.'):
            return False
        if set(p) & PATH_BLOCK:  # someone blocks path
            return False
        return True

    def valid_paths_one(
            self, arr_idx_start: int, slot_idx_start: int
    ) -> tp.Iterator[tuple[str, int, int]]:
        path_block = {'A', 'B', 'C', 'D'}
        ch = self.b[arr_idx_start][slot_idx_start]
        assert ch in path_block

        # see if can move to target room directly.
        # if so, skip all other options as they're going to be more expensive
        target_room_idx = DEST_ROOMS.index(ch)
        target_room = self.rooms[target_room_idx]
        # if already in the target room, can't move anywhere
        if (
            arr_idx_start == target_room_idx + 1
            and set(target_room).issubset({'.', ch})  # room not occupied by anyone else
        ):
            return

        if set(target_room).issubset({'.', ch}):  # room looks fine to move to
            target_room_slot_idx = (target_room.index(ch) if ch in target_room else self.room_len)-1
            path_to_target = self.path(
                arr_idx_start, slot_idx_start, target_room_idx + 1, target_room_slot_idx
            )
            if self.is_valid_path(path_to_target):
                yield path_to_target, target_room_idx + 1, target_room_slot_idx
                return

        # by now we know we can't move to the final place
        # if we're in the hall, we can't move at all
        # if we're in a room, we can move to the hall
        if arr_idx_start:
            # We're in a room. Check if the path is clear
            if slot_idx_start and set(self.b[arr_idx_start][:slot_idx_start]) != {'.'}:
                return

            for target_hall_slot in range(self.hall_len):
                path = self.path(arr_idx_start, slot_idx_start, 0, target_hall_slot)
                if path.endswith('X'):  # can't stop there
                    continue
                if set(path) & path_block:  # someone blocks path
                    continue
                yield path, 0, target_hall_slot


def test_path():
    board = B.from_input("""
#############
#.A.......F.#
###B#C#C#.###
  #A#D#.#D#
  #########
""".strip())
    # hall -> room
    assert board.path(0, 1, 3, 1) == 'X.X.XC.'
    assert board.path(0, 8, 1, 1) == '.X.X.XBA'
    assert board.path(0, 8, 2, 1) == '.X.XCD'

    # room -> hall
    assert board.path(3, 1, 0, 0) == 'CX.X.XA.'
    assert board.path(2, 1, 0, 9) == 'CX.X.XF'

    # room -> room
    assert board.path(3, 1, 1, 1) == 'CX.X.XBA'
    assert board.path(2, 1, 1, 1) == 'CX.XBA'
    assert board.path(1, 1, 4, 1) == 'BX.X.X.X.D'


def test_valid_paths():
    board = B.from_input("""
#############
#.A.......DB#
###B#.#C#.###
  #A#.#C#D#
  #########
""".strip())
    board2 = B.from_input("""
#############
#.A.......D.#
###B#.#C#.###
  #A#B#C#D#
  #########
""".strip())
    board3 = B.from_input("""
#############
#.A.......D.#
###B#C#.#.###
  #A#B#C#D#
  #########
""".strip())
    print(board.vis())
    assert sorted(board.valid_paths_one(1, 1)) == []
    assert sorted(board.valid_paths_one(1, 0)) == [('X.X..', 2, 1)]
    assert sorted(board2.valid_paths_one(1, 0)) == [('X.X.', 2, 0)]
    assert sorted(board.valid_paths_one(0, 10)) == []
    assert sorted(board.valid_paths_one(0, 10)) == []
    assert sorted(board.valid_paths_one(0, 9)) == [('X.', 4, 0)]
    assert sorted(board.valid_paths_one(0, 1)) == []
    assert sorted(board.valid_paths_one(4, 1)) == []
    assert sorted(board.valid_paths_one(3, 0)) == []
    assert sorted(board3.valid_paths_one(1, 0)) == [('X.', 0, 3), ('X.X.', 0, 5), ('X.X.X.', 0, 7)]

    board4 = B.from_input("""
#############
#.....D.....#
###.#B#C#D###
  #A#B#C#A#
  #########
""".strip())
    assert sorted(board4.valid_paths_one(4, 0)) == [('X.', 0, 7), ('X.', 0, 9), ('X..', 0, 10)]


def test_char_positions():
    board = B.from_input("""
#############
#.A.......DB#
###B#.#C#.###
  #A#.#C#D#
  #########
""".strip())

    assert sorted(board.char_positions()) == sorted([
        (0, 1), (0, 9), (0, 10), (1, 0), (1, 1), (3, 0), (3, 1), (4,1)
    ])

    board = B.from_input("""
#############
#.....D.....#
###.#B#C#D###
  #A#B#C#A#
  #########
""".strip())

    assert sorted(board.char_positions()) == sorted([
        (0, 5), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1)
    ])


def test_after_move():
    board = B.from_input("""
#############
#.A.......DB#
###B#.#C#.###
  #A#.#C#D#
  #########
""".strip())

    assert board.after_move(0, 1, 2, 0) == B.from_input("""
#############
#.........DB#
###B#A#C#.###
  #A#.#C#D#
  #########
""".strip())
    assert board.after_move(4, 1, 0, 5) == B.from_input("""
#############
#.A...D...DB#
###B#.#C#.###
  #A#.#C#.#
  #########
""".strip())


def test_is_solved():
    assert not B.from_input("""
    #############
    #.A.......F.#
    ###B#C#C#.###
      #A#D#.#D#
      #########
    """.strip()).is_solved()
    assert B.from_input("""
    #############
    #...........#
    ###A#B#C#D###
      #A#B#C#D#
      #########
    """.strip()).is_solved()
    assert B.from_input("""
    #############
    #...........#
    ###A#B#C#D###
      #A#B#C#D#
      #A#B#C#D#
      #A#B#C#D#
      #########
    """.strip()).is_solved()


def test_cmp():
    board = B.from_input("""
    #############
    #.A.......F.#
    ###B#C#C#.###
      #A#D#.#D#
      #########
    """.strip())

    assert board == B.from_iter('.A.......F.', 'BA', 'CD', 'C.', '.D')

    board = B.from_input("""
    #############
    #.....D.....#
    ###.#B#C#D###
      #A#B#C#A#
      #########
    """.strip())

    assert board == B.from_iter('.....D.....', '.A', 'BB', 'CC', 'DA')


def optimize_cost(board: B) -> int:
    queue = [(board, 0)]
    min_cost = 99999999999999999999999999999
    turns = 0
    mq = 0

    while queue:
        turns += 1
        mq = max(mq, len(queue))
        if turns % 100 == 0:
            sys.stderr.write(".")

        b, cost = queue.pop(0)

        if b in cache and cache[b] <= cost:
            # drop the solution branch
            continue
        cache[b] = cost

        if b.is_solved():
            min_cost = min(min_cost, cost)
            print(f'Solved at {cost}. Min: {min_cost}')
            continue

        for src_array_idx, src_slot in b.char_positions():
            ch = b.b[src_array_idx][src_slot]
            for path, tgt_array_idx, tgt_slot in b.valid_paths_one(src_array_idx, src_slot):
                updated_cost = cost + len(path) * MOVE_COST[ch]
                updated_b = b.after_move(
                    src_array_idx,
                    src_slot,
                    tgt_array_idx,
                    tgt_slot
                )
                queue.append((updated_b, updated_cost))

    print('MQ:', mq)
    return min_cost


def solve(data):
    board = B.from_input(data)
    print(board, '\n')
    print(board.vis())
    print('Optimizing...')
    print(optimize_cost(board))


if __name__ == "__main__":
#     solve("""
# #############
# #...........#
# ###B#C#B#D###
#   #A#D#C#A#
#   #########
#     """.strip())
#     solve("""
# #############
# #...........#
# ###B#C#B#D###
#   #D#C#B#A#
#   #D#B#A#C#
#   #A#D#C#A#
#   #########
#     """.strip())
#     solve("""
# #############
# #...........#
# ###C#D#A#B###
#   #B#A#D#C#
#   #########
#     """.strip())  # answer1: 13556
    solve("""
#############
#...........#
###C#D#A#B###
  #D#C#B#A#
  #D#B#A#C#
  #B#A#D#C#
  #########
    """.strip())  # answer2: 54200
