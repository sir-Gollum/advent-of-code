# coding: utf-8
import argparse
import collections
import dataclasses
from functools import cached_property
from logging import getLogger
from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


CARD_STRENGTHS = '23456789TJQKA'
CARD_STRENGTHS2 = 'J23456789TQKA'


class HandTypes:
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


@dataclasses.dataclass
class Hand:
    cards: str
    bid: int
    p: int = 1

    @classmethod
    def from_line(cls, line: str, p: int = 1) -> 'Hand':
        cards, bid = line.split()
        return cls(cards, int(bid), p)

    @cached_property
    def strongest_joker_combination(self) -> 'Hand':
        if 'J' not in self.cards:
            return self

        winner = self
        for c in CARD_STRENGTHS2:
            new = Hand(self.cards.replace('J', c), self.bid, self.p)
            if new.hand_type > winner.hand_type:
                winner = new

        if winner != self:
            log.debug(
                'Joker: %s -> %s | type: %s -> %s',
                self, winner,
                self.hand_type, winner.hand_type
            )
        return winner

    @cached_property
    def hand_type(self) -> int:
        c = collections.Counter(self.cards)
        counts = sorted(c.values())

        if len(c) == 1:
            # all five cards have the same label
            return HandTypes.FIVE_OF_A_KIND

        if len(c) == 2 and counts == [1, 4]:
            # four cards have the same label and one card has a different label
            return HandTypes.FOUR_OF_A_KIND

        if len(c) == 2 and counts == [2, 3]:
            # three cards have the same label, and the remaining two cards share a different label
            return HandTypes.FULL_HOUSE

        if len(c) == 3 and counts == [1, 1, 3]:
            # three cards have the same label, and the remaining two cards
            # are each different from any other card in the hand
            return HandTypes.THREE_OF_A_KIND

        if len(c) == 3 and counts == [1, 2, 2]:
            # two cards share one label, two other cards share a second label,
            # and the remaining card has a third label
            return HandTypes.TWO_PAIR

        if len(c) == 4 and counts == [1, 1, 1, 2]:
            # two cards share one label, two other cards share a second label,
            # and the remaining card has a third label
            return HandTypes.ONE_PAIR

        if len(c) == 5:
            # all cards' labels are distinct
            return HandTypes.HIGH_CARD

        raise ValueError(f'Unexpected hand: {self.cards}')

    def __lt__(self, other: 'Hand') -> bool:
        this_type = self.hand_type
        other_type = other.hand_type
        strengths = CARD_STRENGTHS
        if self.p != 1:
            this_type = self.strongest_joker_combination.hand_type
            other_type = other.strongest_joker_combination.hand_type
            strengths = CARD_STRENGTHS2

        if this_type < other_type:
            return True

        if this_type == other_type:
            for this_c, other_c in zip(self.cards, other.cards):
                this_str = strengths.index(this_c)
                other_str = strengths.index(other_c)

                if this_str == other_str:
                    continue

                return this_str < other_str

        return False


def main(input_file_name):
    with open(input_file_name) as f:
        lines = f.read().splitlines()

    hands = [Hand.from_line(line) for line in lines]
    hands2 = [Hand.from_line(line, 2) for line in lines]

    log.debug(hands)
    log.debug(f'Hands: {[h.hand_type for h in hands]}')

    answer1 = sum(h.bid * (n + 1) for n, h in enumerate(sorted(hands)))
    answer2 = sum(h.bid * (n + 1) for n, h in enumerate(sorted(hands2)))

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
