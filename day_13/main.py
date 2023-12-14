import re

import numpy as np
from aocd import get_data, submit


def parse_data(data):
    grids = []
    for block in data.split("\n\n"):
        grids.append(block.splitlines())

    return grids


def find_mirror(grid, part2=False):
    for r in range(1, len(grid)):
        above = grid[:r][::-1]
        below = grid[r:]

        above = above[: len(below)]
        below = below[: len(above)]

        if not part2:
            if above == below:
                return r

        elif part2:
            differences = 0
            for x, y in zip(above, below):
                for a, b in zip(x, y):
                    if a != b:
                        differences += 1
            if differences == 1:
                return r

    return 0


def part_1(data):
    grids = parse_data(data)

    solution = 0

    for grid in grids:
        row_count = find_mirror(grid)
        col_count = find_mirror(list(zip(*grid)))

        solution += row_count * 100 + col_count

    print(solution)
    submit(solution, part="a", day=13, year=2023)


def part_2(data):
    grids = parse_data(data)

    solution = 0

    for grid in grids:
        row_count = find_mirror(grid, part2=True)
        col_count = find_mirror(list(zip(*grid)), part2=True)

        solution += row_count * 100 + col_count

    print(solution)
    submit(solution, part="b", day=13, year=2023)


# data = """#.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.

# #...##..#
# #....#..#
# ..##..###
# #####.##.
# #####.##.
# ..##..###
# #....#..#"""

data = get_data(day=13, year=2023)

part_1(data)
part_2(data)
