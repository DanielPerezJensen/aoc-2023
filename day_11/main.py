import re
from itertools import combinations

import numpy as np
from aocd import get_data, submit


def parse_data(data):
    matrix = [[l for l in line] for line in data.splitlines()]

    return matrix


def manhattan_distance(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def part_1(data):
    matrix = parse_data(data)

    empty_rows = [y for y, row in enumerate(matrix) if all(char == "." for char in row)]
    empty_cols = [x for x, cols in enumerate(zip(*matrix)) if all(char == "." for char in cols)]

    width = len(matrix[0])
    for row in reversed(empty_rows):
        matrix.insert(row, ["."] * width)

    height = len(matrix)
    for col in reversed(empty_cols):
        for row in range(height):
            matrix[row] = matrix[row][:col] + ["."] + matrix[row][col:]

    coords = []

    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char == "#":
                coords.append((x, y))

    shortest_paths = [
        manhattan_distance(coord1, coord2) for coord1, coord2 in combinations(coords, 2)
    ]

    solution = sum(shortest_paths)
    print(solution)
    submit(solution, part="a", day=11, year=2023)


def part_2(data):
    pass
    # submit(solution, part="b", day=11, year=2023)


data = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

data = get_data(day=11, year=2023)

part_1(data)
# part_2(data)
