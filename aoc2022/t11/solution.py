# coding: utf-8
import argparse
from functools import reduce
from logging import getLogger
from operator import mul

from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


class Monkey:
    def __init__(self, lines):
        starting_items, op, divby, true_idx, false_idx = None, None, None, None, None
        for line in lines.split('\n'):
            line = line.strip()

            if line.startswith('Starting items: '):
                starting_items = [int(it) for it in line.split(': ')[1].split(',')]

            if line.startswith('Operation: new = '):
                op = line.split(' = ')[1]

            if line.startswith('Test: divisible by '):
                divby = int(line.split()[-1])

            if line.startswith('If true: throw to monkey '):
                true_idx = int(line.split()[-1])

            if line.startswith('If false: throw to monkey'):
                false_idx = int(line.split()[-1])

        assert starting_items is not None
        assert op is not None
        assert divby is not None
        assert true_idx is not None
        assert false_idx is not None

        self.items = starting_items
        self.op = compile(f'lambda old: {op}', 'none', 'eval')
        self.test = lambda x: x % divby == 0
        self.true_idx = true_idx
        self.false_idx = false_idx
        self.inspections = 0

    def turn(self, div_by_three, modulo=None):
        for it in self.items:
            self.inspections += 1
            new = eval(self.op)(old=it)
            if div_by_three:
                new //= 3
            else:
                # https://en.wikipedia.org/wiki/Modular_arithmetic#Congruence
                # example:
                # if monkeys test division by modulo [2, 3, 5, 19], `modulo` is 570
                # and this monkey tests that `new` is divisible by 19,
                # `old` is 97, and the operation is new = old ** 100,
                # then the following two expresions give the same result:
                #   ((old ** 100 ) % modulo) % 19
                #   (old ** 100 ) % 19

                new %= modulo

            test_result = self.test(new)
            if test_result:
                yield new, self.true_idx
            else:
                yield new, self.false_idx


        self.items = []


def game(file_contents, rounds, div_by_three, modulo=None):
    monkeys = [Monkey(lines) for lines in file_contents.split('\n\n')]

    for round in range(rounds):
        log.debug('Round %s', round)
        for n, m in enumerate(monkeys):
            log.debug(
                'Monkey %s inspected items %s times. Items (%s): %s',
                n, m.inspections, len(m.items), m.items
            )

        for m in monkeys:
            for item, idx in m.turn(div_by_three, modulo):
                monkeys[idx].items.append(item)

    log.info('== End of game == ')
    for n, m in enumerate(monkeys):
        log.info(
            'Monkey %s inspected items %s times. Items (%s): %s',
            n, m.inspections, len(m.items), m.items
        )

    most_active = sorted([m.inspections for m in monkeys], reverse=True)[:2]
    return reduce(mul, most_active)


def main(input_file_name):
    with open(input_file_name) as f:
        contents = f.read()

    modulo_parts = []
    for line in contents.splitlines():
        if line.strip().startswith('Test: divisible by '):
            modulo_parts.append(int(line.split()[-1]))

    modulo = reduce(mul, modulo_parts)
    log.debug('Modulo: %s => %s', modulo_parts, modulo)

    answer1 = game(contents, 20, True)
    answer2 = game(contents, 10000, False, modulo)

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename)
