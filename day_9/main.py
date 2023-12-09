import re

import numpy as np
from aocd import get_data, submit


def parse_data(data):
    sequences = []
    for line in data.splitlines():
        sequences.append([int(x) for x in re.findall(r"-?\d+", line)])
    return sequences


def parse_sequence(line, part2=False):
    steps = []
    for i in range(len(line))[:-1]:
        digit = line[i]
        step = int(line[i + 1]) - int(digit)
        steps.append(step)

    return steps


def create_pyramid(sequence, part2=False):
    pyramid = [sequence]
    while not all([x == 0 for x in sequence]):
        sequence = parse_sequence(sequence)
        pyramid.append(sequence)

    return pyramid


def backfill(pyramid):
    pyramid.reverse()

    for i in range(len(pyramid) - 1):
        current_row = pyramid[i]
        next_row = pyramid[i + 1]
        final_value = current_row[-1]
        next_row.append(final_value + next_row[-1])

    return pyramid


def part_1(data):
    sequences = parse_data(data)

    solution = 0

    for sequence in sequences:
        pyramid = create_pyramid(sequence)

        new_sequences = backfill(pyramid)

        solution += new_sequences[-1][-1]

    print(solution)
    submit(solution, part="a", day=9, year=2023)


def part_2(data):
    sequences = parse_data(data)

    solution = 0

    for sequence in sequences:
        sequence.reverse()

        pyramid = create_pyramid(sequence)

        new_sequences = backfill(pyramid)

        solution += new_sequences[-1][-1]

    print(solution)
    submit(solution, part="b", day=9, year=2023)


data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


data = get_data(day=9, year=2023)

part_1(data)
part_2(data)
