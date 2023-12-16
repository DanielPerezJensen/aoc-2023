import re
from functools import cache

import numpy as np
from aocd import get_data, submit
from tqdm import tqdm


def parse_data(data):
    char_map = {"#": 0, ".": 2, "O": 1}

    boulder_map = []
    for line in data.splitlines():
        boulder_map.append([char_map[char] for char in line])

    return boulder_map


def part_1(data):
    boulder_map = parse_data(data)

    columns = list(list(c) for c in zip(*boulder_map))

    solution = 0

    for i, col in enumerate(columns):
        col_str = "".join(map(str, col))
        col_items = col_str.split("0")
        sorted_items = [sorted(item) for item in col_items]

        sorted_str = "0".join("".join(s) for s in sorted_items)

        for i in range(len(sorted_str)):
            if sorted_str[::-1][i] == "1":
                solution += i + 1

    print(solution)

    submit(solution, part="a", day=14, year=2023)


char_map = {"#": 0, ".": 2, "O": 1}


def split_tuple(x, split_char):
    result = []
    temp_list = []
    for i in x:
        if i == split_char:
            result.append(temp_list)
            temp_list = []
        else:
            temp_list.append(i)
    result.append(temp_list)

    return result


def chain(*iterables):
    for it in iterables:
        for each in it:
            yield each
        yield 0


@cache
def roll_direction(boulder_map, dir="n"):
    new_boulder_map = []

    if dir == "n":
        columns = list(list(c) for c in zip(*boulder_map))

        for i, col in enumerate(columns):
            col_items = split_tuple(col, 0)

            sorted_items = [sorted(item) for item in col_items]
            sorted_items_flattened = tuple(chain(*sorted_items))[:-1]
            new_boulder_map.append(sorted_items_flattened)

        new_boulder_map = tuple(tuple(c) for c in zip(*new_boulder_map))

    elif dir == "w":
        for row in boulder_map:
            row_items = split_tuple(row, 0)
            sorted_items = [sorted(item) for item in row_items]
            sorted_items_flattened = tuple(chain(*sorted_items))[:-1]
            new_boulder_map.append(sorted_items_flattened)

    elif dir == "s":
        columns = list(list(c) for c in zip(*boulder_map))

        for i, col in enumerate(columns):
            col_items = split_tuple(col, 0)
            sorted_items = [sorted(item, reverse=True) for item in col_items]
            sorted_items_flattened = tuple(chain(*sorted_items))[:-1]
            new_boulder_map.append(sorted_items_flattened)

        new_boulder_map = tuple(tuple(c) for c in zip(*new_boulder_map))

    elif dir == "e":
        for row in boulder_map:
            row_items = split_tuple(row, 0)
            sorted_items = [sorted(item, reverse=True) for item in row_items]
            sorted_items_flattened = tuple(chain(*sorted_items))[:-1]
            new_boulder_map.append(sorted_items_flattened)

    return tuple(new_boulder_map)


@cache
def run_loop(boulder_map):
    boulder_map = roll_direction(boulder_map, dir="n")
    boulder_map = roll_direction(boulder_map, dir="w")
    boulder_map = roll_direction(boulder_map, dir="s")
    boulder_map = roll_direction(boulder_map, dir="e")

    return boulder_map


def part_2(data):
    reverse_char_map = {0: "#", 2: ".", 1: "O"}

    boulder_map = parse_data(data)
    boulder_map = tuple(tuple(s) for s in boulder_map)

    seen = {}

    iterations = 1_000

    for i in range(iterations):
        boulder_map = run_loop(boulder_map)

    solution = 0

    for col in list(zip(*boulder_map)):
        for i, row in enumerate(col[::-1]):
            if row == 1:
                solution += i + 1

    print(solution)
    submit(solution, part="b", day=14, year=2023)


data = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


data = get_data(day=14, year=2023)

part_1(data)
part_2(data)
