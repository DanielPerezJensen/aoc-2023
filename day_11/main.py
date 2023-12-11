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

    expansion_factor = 2

    expanded_coords = []

    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char == "#":
                new_x, new_y = expand_coords((x, y), expansion_factor, empty_rows, empty_cols)
                expanded_coords.append((new_x, new_y))

    shortest_paths = [
        manhattan_distance(coord1, coord2) for coord1, coord2 in combinations(expanded_coords, 2)
    ]

    solution = sum(shortest_paths)
    print(solution)
    submit(solution, part="a", day=11, year=2023)


def expand_coords(coords, expansion_factor, empty_rows, empty_cols):
    empty_cols_before = sum([1 for col in empty_cols if col < coords[0]])
    empty_rows_before = sum([1 for row in empty_rows if row < coords[1]])

    return (
        coords[0] + empty_cols_before * (expansion_factor - 1),
        coords[1] + empty_rows_before * (expansion_factor - 1),
    )


def part_2(data):
    matrix = parse_data(data)

    empty_rows = [y for y, row in enumerate(matrix) if all(char == "." for char in row)]
    empty_cols = [x for x, cols in enumerate(zip(*matrix)) if all(char == "." for char in cols)]

    expansion_factor = 1_000_000

    expanded_coords = []

    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char == "#":
                new_x, new_y = expand_coords((x, y), expansion_factor, empty_rows, empty_cols)
                expanded_coords.append((new_x, new_y))

    shortest_paths = [
        manhattan_distance(coord1, coord2) for coord1, coord2 in combinations(expanded_coords, 2)
    ]

    solution = sum(shortest_paths)
    print(solution)
    submit(solution, part="b", day=11, year=2023)


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
part_2(data)
