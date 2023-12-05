# coding: utf-8
import argparse
import dataclasses
from logging import getLogger
from typing import Optional

from aocutils.debug import configure_logging, DEBUG, INFO
from aocutils.iteration import chunkwise

log = getLogger()


@dataclasses.dataclass
class Range:
    start: int
    length: int

    @property
    def end(self):
        # last number included in the interval
        return self.start + self.length - 1

    def __hash__(self) -> int:
        return hash((self.start, self.length))


@dataclasses.dataclass
class Mapping:
    dst_start: int
    src_start: int
    length: int

    @property
    def src_end(self):
        # last number included in the interval
        return self.src_start + self.length - 1

    @property
    def dst_end(self):
        # last number included in the interval
        return self.dst_start + self.length - 1

    def convert(self, num: int) -> Optional[int]:
        if self.src_start <= num <= self.src_end:
            return self.dst_start + num - self.src_start

    def convert_range(self, rng: Range) -> tuple[Optional[Range], Optional[Range]]:
        # no overlap => no conversion
        if rng.start >= self.src_end or rng.end <= self.src_start:
            return None, rng

        # fully contained => full conversion
        if self.src_start <= rng.start and self.src_end >= rng.end:
            converted = Range(
                start=self.dst_start + rng.start - self.src_start,
                length=rng.length
            )
            return converted, None

        # some overlap
        if self.src_start >= rng.start:
            # rng is to the left
            inside = Range(
                start=self.dst_start,
                length=rng.end - self.src_start + 1
            )

            outside = Range(
                start=rng.start,
                length=self.src_start - rng.start
            )
            assert inside.length + outside.length == rng.length
            return inside, outside
        else:
            # rng is to the right
            inside = Range(
                start=self.dst_start + rng.start - self.src_start,
                length=self.src_end - rng.start + 1
            )

            outside = Range(
                start=self.src_end + 1,
                length=rng.end - self.src_end
            )
            assert inside.length + outside.length == rng.length

            return inside, outside

    @staticmethod
    def convert_ranges(
            ranges: set[Range], mappings: list['Mapping']
    ) -> set[Range]:
        result = set()

        while True:
            original_range, converted_range, split_range = None, None, None

            for original_range in ranges:
                for m in mappings:
                    converted_range, split_range = m.convert_range(original_range)
                    if converted_range:
                        log.debug('Map %s Conversion: %s -> %s', m, original_range, converted_range)
                        result.add(converted_range)
                        break

                if converted_range:
                    break
            else:
                result |= ranges
                return result

            if converted_range:
                ranges.remove(original_range)

            if split_range:
                ranges.add(split_range)


def main(input_file_name):
    with open(input_file_name) as f:
        sections = f.read().strip().split('\n\n')

    seeds = [int(s) for s in sections[0].split()[1:]]
    log.info('Initial seeds: %s', seeds)

    seed_ranges = {Range(*it) for it in chunkwise(seeds, 2)}
    log.info('Seeds range: %s', seed_ranges)

    for map_section in sections[1:]:
        map_name = map_section.split('\n')[0]
        map_lines = map_section.split('\n')[1:]
        mappings = [Mapping(*map(int, line.split())) for line in map_lines]

        # part 1
        new_seeds = []
        for m in mappings:
            for s in seeds[:]:
                converted = m.convert(s)
                if converted:
                    while s in seeds:
                        new_seeds.append(converted)
                        seeds.remove(s)

        log.debug('%30s | Not converted seeds: %s', map_name, seeds)
        new_seeds += seeds
        seeds = new_seeds
        log.debug('%30s | Seeds after conversion: %s', map_name, new_seeds)

        # part 2
        seed_ranges = Mapping.convert_ranges(seed_ranges, mappings)
        log.debug('%30s | (2) Seed ranges after conversion: %s', map_name, seed_ranges)

    answer1 = min(seeds)
    answer2 = min(r.start for r in seed_ranges)

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
