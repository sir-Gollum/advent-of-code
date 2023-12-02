# coding: utf-8
import argparse
import dataclasses
from logging import getLogger
import typing as t
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


@dataclasses.dataclass
class RGB:
    r: int = 0
    g: int = 0
    b: int = 0


@dataclasses.dataclass
class Game:
    id: int
    draws: list[t.Any]

    @staticmethod
    def _parse_draw(draw: str) -> RGB:
        draw_items = draw.strip().split(', ')
        parsed = RGB()
        for it in draw_items:
            parts = it.split()
            match parts[1]:
                case 'red':
                    parsed.r += int(parts[0])
                case 'green':
                    parsed.g += int(parts[0])
                case 'blue':
                    parsed.b += int(parts[0])
                case _:
                    raise ValueError(f'Error parsing draw: {draw}')
        return parsed

    @classmethod
    def from_string(cls, s: str) -> 'Game':
        game_id = int(s.strip().split(':')[0].split()[1])
        draws = [cls._parse_draw(d) for d in s.split(':')[1].split(';')]
        log.debug(f'id: {game_id}, draws: {draws}')
        return cls(game_id, draws)

    def is_possible(self, constraints: RGB) -> bool:
        for draw in self.draws:
            if draw.r > constraints.r or draw.g > constraints.g or draw.b > constraints.b:
                return False
        return True

    def get_power(self):
        constraint = RGB()
        for draw in self.draws:
            constraint.r = max(draw.r, constraint.r)
            constraint.g = max(draw.g, constraint.g)
            constraint.b = max(draw.b, constraint.b)
        return constraint.r * constraint.g * constraint.b


def main(input_file_name):
    part1_constraint = RGB(r=12, g=13, b=14)
    answer1, answer2 = 0, 0

    with open(input_file_name) as f:
        for line in f:
            g = Game.from_string(line)
            answer1 += g.id if g.is_possible(part1_constraint) else 0
            answer2 += g.get_power()

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
