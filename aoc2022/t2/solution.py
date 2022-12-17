# coding: utf-8
import sys

# A,X = rock
# B,Y = paper
# C,Z = scissors
LOOKUP1 = {
    'X': 1,
    'Y': 2,
    'Z': 3,
    ('A', 'X'): 3,
    ('A', 'Y'): 6,
    ('A', 'Z'): 0,
    ('B', 'X'): 0,
    ('B', 'Y'): 3,
    ('B', 'Z'): 6,
    ('C', 'X'): 6,
    ('C', 'Y'): 0,
    ('C', 'Z'): 3,
}


LOOKUP2 = {
    ('A', 'X'): 0 + LOOKUP1['Z'],
    ('A', 'Y'): 3 + LOOKUP1['X'],
    ('A', 'Z'): 6 + LOOKUP1['Y'],
    ('B', 'X'): 0 + LOOKUP1['X'],
    ('B', 'Y'): 3 + LOOKUP1['Y'],
    ('B', 'Z'): 6 + LOOKUP1['Z'],
    ('C', 'X'): 0 + LOOKUP1['Y'],
    ('C', 'Y'): 3 + LOOKUP1['Z'],
    ('C', 'Z'): 6 + LOOKUP1['X'],
}


def main(input_file_name):
    strategy = [l.split() for l in open(input_file_name)]

    score = 0
    for their, mine in strategy:
        score += LOOKUP1[mine] + LOOKUP1[(their, mine)]

    if len(strategy) < 100:
        print('Strat:', strategy)

    print('Answer 1:', score)

    #  part 2
    score = 0
    for their, mine in strategy:
        score += LOOKUP2[(their, mine)]

    print('Answer 2:', score)


if __name__ == '__main__':
    main(sys.argv[1])
