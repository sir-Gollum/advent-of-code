# coding: utf-8
import argparse
import re
from logging import getLogger

from aocutils.debug import configure_logging, DEBUG, INFO

log = getLogger()


def get_result(monkeys, key):
    if isinstance(monkeys[key], int):
        return monkeys[key], None, None

    equation = monkeys[key]
    a, op, b = equation.split()
    a_value, _, _ = get_result(monkeys, a)
    b_value, _, _ = get_result(monkeys, b)

    return eval(f'int({a_value} {op} {b_value})'), a_value, b_value


def find_humn(monkeys):
    root, humn = 'root', 'humn'
    monkeys[root] = re.sub(r' [^ ]+ ', ' == ', monkeys[root])

    def check(v):
        monkeys[humn] = v
        res, a, b = get_result(monkeys, root)
        return a - b

    # simplified "gradient descent"-like search
    cur = 0
    d = max(check(cur) // 10000, 1)

    while True:
        v_cur = check(cur)
        v_next = check(cur + d)

        if v_next == 0:
            result = cur + d
            log.debug(f'Found valid humn: {result}, searching nearby for a smaller value')

            min_result = result
            for i in range(50):
                if check(result - i - 1) == 0:
                    min_result = result - i - 1

            log.debug(f'After searching for a near smaller value, result is {min_result}')
            return min_result

        cur += d
        log.debug(f'd={d}, cur={cur}, next={v_next}')
        if abs(v_next) > abs(v_cur):
            if d // 2 in {0, -1}:
                d = -d // d
            else:
                d = -d // 2
            log.debug(f'Flip d={d}')


def plot_humn(monkeys):
    # monte carlo-like plotting
    root, humn = 'root', 'humn'
    monkeys[root] = re.sub(r' [^ ]+ ', ' == ', monkeys[root])

    def check(v):
        monkeys[humn] = v
        res, a, b = get_result(monkeys, root)
        return a - b

    import matplotlib.pyplot as plt
    import random
    random.seed()

    fig, ax = plt.subplots()
    answer = 3353687996515
    delta = 10000
    x_min, x_max = answer - delta, answer + delta
    ax.set_xlabel('humn')
    ax.set_ylabel('delta (should be 0)')

    ax.plot(answer, check(answer), 'bo')
    for pt in range(500):
        x = random.randint(x_min, x_max)
        y = check(x)
        ax.plot(x, y, 'ro')

    plt.show()


def main(input_file_name, plot=False):
    monkeys = {}
    with open(input_file_name) as f:
        for line in f:
            name, value = line.strip().split(': ')
            try:
                monkeys[name] = int(value)
            except ValueError:
                monkeys[name] = value.replace('/', '//')

    # part 1
    log.debug(f'Monkeys: {monkeys}')
    answer1, _, _ = get_result(monkeys, 'root')

    # part 2
    answer2 = find_humn(monkeys)

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)
    if plot:
        plot_humn(monkeys)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-p', '--plot', action='store_true')
    args = parser.parse_args()

    configure_logging(DEBUG if args.debug else INFO)
    main(args.filename, plot=args.plot)
