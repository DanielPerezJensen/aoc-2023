import re
from functools import cache

import numpy as np
from aocd import get_data, submit
from tqdm import tqdm


def parse_data(data):
    springs_clues = []
    for line in data.splitlines():
        left, right = line.split(" ")
        clues = tuple(int(clues) for clues in right.split(","))
        springs_clues.append((left, clues))

    return springs_clues


memory = {}


@cache
def arrangement_counts(springs, clues):
    if (springs, clues) in memory:
        return memory[(springs, clues)]

    # ['', ()] is legal
    if len(springs) == 0:
        memory[(springs, clues)] = len(clues) == 0
        return len(clues) == 0

    # [springs, ()] is legal so long as springs has no '#'
    if len(clues) == 0:
        memory[(springs, clues)] = "#" not in springs
        return "#" not in springs

    if springs[0] == ".":
        return arrangement_counts(springs[1:], clues)

    if springs[0] == "?":
        # replace ? with either # or .
        count_dot = arrangement_counts(springs[1:], clues)
        count_hash = arrangement_counts("#" + springs[1:], clues)
        memory[(springs, clues)] = count_dot + count_hash
        return count_dot + count_hash

    # springs starts with '#'
    if springs[0] == "#":
        if len(springs) < clues[0]:
            memory[(springs, clues)] = 0
            return 0
        if "." in springs[: clues[0]]:
            memory[(springs, clues)] = 0
            return 0  # impossible - not enough space for the spring
        # If there is one spring left, it must be the last one in the clue
        if len(springs) == clues[0]:
            memory[(springs, clues)] = len(clues) == 1
            return len(clues) == 1
        if springs[clues[0]] not in "?.":
            memory[(springs, clues)] = 0
            return 0  # springs must be separated by '.' (or '?')

        # in case it passes all this
        return arrangement_counts(springs[clues[0] + 1 :], clues[1:])  # one less spring

    # replace ? with either # or .
    count_dot = arrangement_counts(springs[1:], clues)
    count_hash = arrangement_counts("#" + springs[1:], clues)
    return count_dot + count_hash


def part_1(data):
    springs_clues = parse_data(data)

    solution = sum((arrangement_counts(spring, clue) for spring, clue in springs_clues))

    submit(solution, part="a", day=12, year=2023)


def part_2(data):
    springs_clues = parse_data(data)

    new_springs_clues = [[(spring + "?") * 4 + spring, clue * 5] for spring, clue in springs_clues]

    solution = sum((arrangement_counts(spring, clue) for spring, clue in new_springs_clues))

    submit(solution, part="b", day=12, year=2023)


data = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


data = get_data(day=12, year=2023)

part_1(data)
part_2(data)
