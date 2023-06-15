# coding: utf-8
"""
--- Day 24: Arithmetic Logic Unit ---

Magic smoke starts leaking from the submarine's arithmetic logic unit (ALU). Without the ability to perform basic arithmetic and logic functions, the submarine can't produce cool patterns with its Christmas lights!

It also can't navigate. Or run the oxygen system.

Don't worry, though - you probably have enough oxygen left to give you enough time to build a new ALU.

The ALU is a four-dimensional processing unit: it has integer variables w, x, y, and z. These variables all start with the value 0. The ALU also supports six instructions:

inp a - Read an input value and write it to variable a.
add a b - Add the value of a to the value of b, then store the result in variable a.
mul a b - Multiply the value of a by the value of b, then store the result in variable a.
div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
In all of these instructions, a and b are placeholders; a will always be the variable where the result of the operation is stored (one of w, x, y, or z), while b can be either a variable or a number. Numbers can be positive or negative, but will always be integers.

The ALU has no jump instructions; in an ALU program, every instruction is run exactly once in order from top to bottom. The program halts after the last instruction has finished executing.

(Program authors should be especially cautious; attempting to execute div with b=0 or attempting to execute mod with a<0 or b<=0 will cause the program to crash and might even damage the ALU. These operations are never intended in any serious ALU program.)

For example, here is an ALU program which takes an input number, negates it, and stores it in x:

inp x
mul x -1
Here is an ALU program which takes two input numbers, then sets z to 1 if the second input number is three times larger than the first input number, or sets z to 0 otherwise:

inp z
inp x
mul z 3
eql z x
Here is an ALU program which takes a non-negative integer as input, converts it into binary, and stores the lowest (1's) bit in z, the second-lowest (2's) bit in y, the third-lowest (4's) bit in x, and the fourth-lowest (8's) bit in w:

inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
Once you have built a replacement ALU, you can install it in the submarine, which will immediately resume what it was doing when the ALU failed: validating the submarine's model number. To do this, the ALU will run the MOdel Number Automatic Detector program (MONAD, your puzzle input).

Submarine model numbers are always fourteen-digit numbers consisting only of digits 1 through 9. The digit 0 cannot appear in a model number.

When MONAD checks a hypothetical fourteen-digit model number, it uses fourteen separate inp instructions, each expecting a single digit of the model number in order of most to least significant. (So, to check the model number 13579246899999, you would give 1 to the first inp instruction, 3 to the second inp instruction, 5 to the third inp instruction, and so on.) This means that when operating MONAD, each input instruction should only ever be given an integer value of at least 1 and at most 9.

Then, after MONAD has finished running all of its instructions, it will indicate that the model number was valid by leaving a 0 in variable z. However, if the model number was invalid, it will leave some other non-zero value in z.

MONAD imposes additional, mysterious restrictions on model numbers, and legend says the last copy of the MONAD documentation was eaten by a tanuki. You'll need to figure out what MONAD does some other way.

To enable as many submarine features as possible, find the largest valid fourteen-digit model number that contains no 0 digits. What is the largest model number accepted by MONAD?

Your puzzle answer was 74929995999389.

--- Part Two ---

As the submarine starts booting up things like the Retro Encabulator, you realize that maybe you don't need all these submarine features after all.

What is the smallest model number accepted by MONAD?

Your puzzle answer was 11118151637112.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

from collections import defaultdict
from typing import List


CONSTS = [
    [1, 11, 14],
    [1, 13, 8],
    [1, 11, 4],
    [1, 10, 10],
    [26, -3, 14],
    [26, -4, 10],
    [1, 12, 4],
    [26, -8, 14],
    [26, -3, 1],
    [26, -12, 6],
    [1, 14, 0],
    [26, -6, 9],
    [1, 11, 13],
    [26, -12, 12],
]


def interpret(instructions: List[str], input_data: List[int]):
    if any([i == 0 for i in input_data]):
        raise ValueError(f'Invalid input: {input_data}')

    reg = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    input_iter = iter(input_data)

    for instr_line in instructions:
        instr, _, args = instr_line.strip().partition(' ')
        if instr == 'inp':
            var = args
            reg[var] = next(input_iter)
        else:
            arg0, arg1 = args.split()
            if arg1 in reg:
                arg1 = reg[arg1]
            else:
                arg1 = int(arg1)

            if instr == 'mul':
                reg[arg0] *= arg1
            elif instr == 'add':
                reg[arg0] += arg1
            elif instr == 'mod':
                reg[arg0] %= arg1
            elif instr == 'div':
                reg[arg0] = int(reg[arg0] / arg1)
            elif instr == 'eql':
                reg[arg0] = int(reg[arg0] == arg1)

    return reg['w'], reg['x'], reg['y'], reg['z']


def generate_formulas(instructions):
    input_data = []
    for instr in instructions:
        if instr.startswith('inp '):
            input_data.append(f'N{len(input_data)+1}')

    reg = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    input_iter = iter(input_data)

    for instr_line in instructions:
        instr, _, args = instr_line.strip().partition(' ')
        if instr == 'inp':
            var = args
            reg[var] = next(input_iter)
        else:
            arg0, arg1 = args.split()
            if arg1 in reg:
                arg1 = reg[arg1]

            if instr == 'mul':
                if arg1 == '0':
                    reg[arg0] = '0'
                else:
                    reg[arg0] = f'({reg[arg0]}) * ({arg1})'
            elif instr == 'add':
                if reg[arg0] == '0':
                    reg[arg0] = arg1
                else:
                    reg[arg0] = f'({reg[arg0]}) + ({arg1})'
            elif instr == 'mod':
                reg[arg0] = f'({reg[arg0]}) % ({arg1})'
            elif instr == 'div':
                if arg1 != '1':
                    reg[arg0] = f'int(({reg[arg0]}) / ({arg1}))'
            elif instr == 'eql':
                reg[arg0] = f'int(({reg[arg0]}) == ({arg1}))'

    return reg['w'], reg['x'], reg['y'], reg['z']


def prog(input_data: List[int]):
    w, x, y, z = 0, 0, 0, 0
    for step, w in enumerate(input_data):
        div_z, add_x, add_y = CONSTS[step]

        x = int((z % 26 + add_x) != w)
        z = int(z/div_z) * (25 * x + 1) + (w + add_y) * x

    return z


def reverse_prog():
    # (target_z_value, input_as_string_so_far) pairs
    reversed_chains = {14: {0: ['']}}

    for digit_idx in range(13, -1, -1):
        print(f'\nProcessing digit {digit_idx}')
        div_z, add_x, add_y = CONSTS[digit_idx]
        reversed_chains[digit_idx] = defaultdict(list)

        for initial_z in range(1_000_000):
            for w in range(1, 10):
                x = int((initial_z % 26 + add_x) != w)
                new_z = int(initial_z / div_z) * (25 * x + 1) + (w + add_y) * x

                # new_z leads to eventually having 0 in z, record paths leading to it
                if new_z in reversed_chains[digit_idx+1]:
                    for it in reversed_chains[digit_idx + 1][new_z]:
                        reversed_chains[digit_idx][initial_z].append(str(w) + it)

    largest_mond = max(i for it in reversed_chains[0].values() for i in it)
    smallest_monad = min(i for it in reversed_chains[0].values() for i in it)
    print(f'Largest: {largest_mond}, smallest: {smallest_monad}')


def solve1(instructions):
    reverse_prog()


if __name__ == "__main__":
    solve1("""
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 14
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -3
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 14
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -4
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -8
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 14
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -3
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 0
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -6
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y    
    """.strip().splitlines())
