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
    # print(new_col)

    # submit(solution, part="a", day=14, year=2023)


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


@cache
def roll_direction(boulder_map, dir="n"):
    new_boulder_map = []

    if dir == "n":
        columns = list(list(c) for c in zip(*boulder_map))

        for i, col in enumerate(columns):
            col_items = split_tuple(col, 0)

            print(col_items)

            sorted_items = [sorted(item) + [0] for item in col_items]
            sorted_items_flattened = list(chain(*sorted_items))
            # print(sorted_items_flattened)
            new_boulder_map.append(tuple(sorted_items_flattened))

        new_boulder_map = tuple(tuple(c) for c in zip(*new_boulder_map))

    elif dir == "s":
        columns = list(list(c) for c in zip(*boulder_map))

        for i, col in enumerate(columns):
            col_str = "".join(map(str, col))
            col_items = col_str.split("0")
            sorted_items = [sorted(item, reverse=True) for item in col_items]
            sorted_str = "0".join("".join(s) for s in sorted_items)
            new_boulder_map.append(tuple(int(s) for s in sorted_str))

        new_boulder_map = tuple(tuple(c) for c in zip(*new_boulder_map))

    return new_boulder_map


seen = dict()


@cache
def run_loop(boulder_map):
    boulder_map = roll_direction(boulder_map, dir="n")
    boulder_map = roll_direction(boulder_map, dir="s")

    return boulder_map


def part_2(data):
    reverse_char_map = {0: "#", 2: ".", 1: "O"}

    boulder_map = parse_data(data)
    boulder_map = tuple(tuple(s) for s in boulder_map)

    # for _ in tqdm(range(1_000_000_000)):
    #     new_boulder_map = run_loop(boulder_map)

    for col in boulder_map:
        print(" ".join(list(reverse_char_map[c] for c in col)))

    new_boulder_map = roll_direction(boulder_map, dir="n")

    print("*" * 25)

    for col in new_boulder_map:
        print(" ".join(list(reverse_char_map[c] for c in col)))

    # submit(solution, part="b", day=14, year=2023)


data = """.#.OO.O.#OO........O....O..OO....OOO...#....#..........#.O.OO.....O#.#..#..#O##.O..#.#.O#.O.OO.....#
.O##.#..O..##..#..#.#..O#....O##..#.....##.......O...O#O..O.......#..#..O#O...#O..OO.#.....O.##.#.##
#.O...O.#.O....#.O..#OO...O...#.#.##...........#....#O.....##..#.O.#.............O...O..O.O...##...#
.#.#.....O..#...#...O.####OO....#.O...O...O...O.....OO#.O.##O.............O...#O.#OO#......O........
OO.O.....O....O..OO..O#..OO.OOO..OO...........O..##.O...O.#.O...##.O##....O.OO.#.O.....O..#.O...O##O
.#..##....#.O#...........#..OO...O......O.......#O..O..#...O......#.#....#.OO#..#O...O...#.....O..O#
##..OO.##.#........OOO##...OO.OOO#O...OOO.O.O...#...#.##..O##...#.#O#....#........#.O....#O.#O.O..O.
...O.O.O#...O.....O..OO...#O..#.#...O......#.......#.O...O.O#....O......#.OO.O..OOO.OO.O.O.###O...OO
...#O.....#O..##..#O.#...O.#...OO#O#.#..#.#....O..O.O.#...O.O...O.#..##O...O.#.OO.#O...OO.O.#O.OO#..
#.....#.#.O..#....O....##.O#......OO#....O#.#O.#..#O..#OO..#O..O...##O..#.....O##...O#.#..OO....O..#
.#OOO...#O...#...##...#O....#O..........O.#.O.O#..#..#OO.#............#....O#.#O....#....OO..#...O.O
#...OO...O...O..O.#.........O#O##..O........O.#..#O#O.##....#...#O.....OOO.#......#....O.O..#.OO.#..
.OO.....#..##...#.O.#O.#...##..#...#O.#...O#........O.O....#.##....O...#..#...#.O....OO..OO....O..#.
#..#.....OO....#O.#.O...O.OOO..O..O.#.O...OOOO..O.O...#..OOO...#......#.###.O.O....O.......O....O.#.
.#O.#....O....O#.OO..O.OOO...........O.##........O#O..#...O.#...O....O..O.##.#O#.#OO.O...O#...#..#O.
.OO.#O.#..O.O.OO...O.O....OOOO#.O.O.#.#.O.#.#....OO.#....#..#.....##...O....OO.OO...#.O.O...O.....OO
...###..O......#O.....#.....#...O.......O.#O.O..#..........OO..O.#..O...#..#.O.O....#..#.#...O.OOO..
........O..O.......O.......O#.O.O...#.#....#........#.#....OO....#.#........###.#...O...#OO.O#.#....
.OO#...........#......#.......#....O......#......##.O......OO.O#...O...O....O######O#..O..O.....OO..
.O.........OOO#O.#O...#.O....OOO##.......O.#..O..#..#O........O.OO..O..#...#O#..##..O#.###....OO....
.#.#.#O..#..#OO...O......O....OO..O......O......#..O..#...O.#..O...#....OOO....OO.OO#O....O.#.......
..OO..O.O..O#..#......OO.........#.O..O.O..#......#OO.#..O.O.#O#..O.#O...O.O..O.#......O...OOO.OO..#
O.O##....O.O....#.....#...OO..O..#.##..O..O###....#...O.#.O#O.OO.OO#.#...#.....#.#....O...#OOO..O#..
#.#.O.#O.O#.#...O..OOO.O.#.#......O..#O.#..##.##..#.........O...#OO...#..O.....#O...O..##O#O........
..O#O.##O.O.#.....#.OO..O.....OOOO#O....O..O.##O#..O..#..O#....##OO#..O...O..##..#O.##.........O#..O
#.#.#..##..O.O#O...##.#.O....#..#.O#..#....O.....#.#.....#.O.#O.....O.#.##...#..O.O.OOO..O...O......
....#....O..OO.#...O.O#.#.##..O....O..OO.#....O...O...O.....#......#..OO#OO.OO#..#.O#....#.#.OO..##O
O.##O.O.O....O..#......O..O.#O#O....#O....#.#.#.#O.........OO..O....O.#......O##OO......OOO..#O..#..
#.O.O.OO.O..#.....#O..#......O.......#....O.....O.....#...O.#.O......#...###...OO.#..O.OO#.O#..O#.OO
.....O.#.##OOOOOO#.#OO#O..#...#.........O..O.OO...OO....O..O.......O..O...#.#OO#.O.........O......O.
O......#..OO.O..O.......#..#...#..O.OO.#..##..#.O...#.O.#.O#O##.O.#.#..#..#....O.....#.#..O.....O#..
#.....#O...O.O......O......O.O.OO.O#O..#...O..#....#.....#O..O..#O...O..O.OO##.#.##O.#..#..#.#.....O
O#.O##..###.........O.....O.#.O#....#O.O..O.O#O#....OO..#O..O.....OO.O##..OO.#......#.O......###....
..O....#...OO.OO#.O#.O.OO#..O...##..OO..O#O#..OO..#.....OO...........O....#...#.......O#....O#......
....#.#O.O..OO......##.OO.#..##O.....#.......#.........O.O..OO.OO...#.#O.#O...OOOOO..O...OOOO.O#.#..
....#O##.OO#O..O.O.O#O.#O#..###....OO.....#OO..O.........O.O....OO.O..#..O#..OO...O#O.O.O.......O#..
O.O#.O.#.OO....OOO.O.O.O...OO.#.O.##..O..O.#..OO.#..O............#O.##.O#.OO.O.##..#....#..OO.O...#.
.#...O.#.#.#.O.#..##.O##.#..O..O...#.......O...OO.....#...#.OO#..O.OO....O....O.....#O.O#OO.##OO..O.
O#OO.OO..O..O.......O#.O....OO...O.........OO#.#O#O#.OO....#..#...O...OOO#...O.#O.#...........OO.O#.
..OO#..O...OO#O..#..#.#...#......O....O#..O.O....O#...##.....O..#O#..........O#.#......#.#.#OOO..O.O
.OO.......OO.#...O...O#.O...#..OO.##........O.........O..OOO.O..#......O#.OO.O....O.#..OOO....O..O.O
O#.O.#..O#..#O.#..O.O...##...O#.#O#...#O......O#.....#.###..#....O.....#O#....#....O#.O.O..#OO.O...O
.O...O...O...O.#.OO....#...O.O..........O...#...#........##..........##...#..O.O.O#O#.#......O..O...
.#.#..#O.#.....O.#....##........#....#....O.#O.O..............O.O....#..O.O.#O....O#O........#....O.
O....###O...O..O...OO.....#......O#.O..OO.#.#.O#....#O..#.O..OO..#..O.#.O..#....O...#OO.....O.OO.O..
#O.O.O.#O...#.OO...........#....O...#O.......#...##..##.##.O.O..........OOO..O..#..OO..O..OO..#.#.#.
#.O#..#..O.OOOO....OO.#O##.##..#..OO##O#.#.O....O.O#.##.O#...OO.O......#..#...O........O...#.##O..#.
......#...O......#......O.#..O.OOOO.O.O......#.#O...O#....O..#...........O.O..#...#..#O..O.O..##O..O
..O.#.....#...O.O..O....O.....#.....#.....O..O.O.O#O.#.....#.#OOOO...O.....O.#..#O..O.OOO....#OOO.O.
.OOO....O#.........O.......#..O......#..........#...##O...O...O...O.O.O##....O#O##.......##O...#..O.
#.##.O.O....O......##..#.....##..##..O#....O.#O#.O....#........#.#.#....OO.O.........OO..O......#O#.
#.O.......#O#.O....O.O.......O.O##O#....#O.O.#O#.O.O.OO..#.O#...O.##.###.O.O#.O..#...#O.....OO....##
..O......O...#..#.O#....##O......OO......O.O....O....O#...O.O.OOO.#O...O.#..O......OO...#.O#.....#.O
.OO...#O.O....O.........##......##.......#...O..##.....#...OO.....O...#.#....O..O...O#.......O..O.O.
.O#.....O....O..O...#.O.O#...#.#..#O#.O.....O#O.OO....#....O..OO.OO.#..#.#.O.O.....O..O......O..#..#
.O.#...O...O.OOO#O...#........O..#..#.##..#...#...#..O....##.O.O#...O.....O.##.O........O...#O#O#.O.
.#O....#.O#O##O......O........#...##.#..O.OO..O.....#.#.O#...O.O#.#...#.......#...#.#.O.....O.OOO...
.O....OO###...O#...O..#..O............#O.#.O.......OO...O...##......O.#..O.O#.#....O..O.#....O...##O
#..#O#.O...O....OO..O..........OO##.....O......O...##O.#..O..OO#...#.OO..#...#.O..O...O.O#.....#....
O.O#OO.....O#.O..##.OOO.##....O#...O..#.#...O..OO......O#..O..O..#...#O........##.O##....#O.....OO.O
......O..O..O....OOO..O...O.O#..#.....O..O..#....#.O##....O.#..##O...O..O..OO....#...O.#..O..OO...#.
..........O.#O#.#......#......#O..O.O.OOOOO.#...O..#.O.OO....#.O#.#O..#......#.#O.O.O...O..##..O#.O.
OO#...#...OOO..O.#.......#.O...##..O.O......#..O.......##.....O..O.....OOO.##..O..O.#...#O.......#.#
....##..#..O......OO.......O#O#O...O.O.#.#..#..##..##O....O.#.........#.O...#..O........O..#..#O.OO.
......O.O...OO##..O..##.O#O#..O##.O#..#...O##....#.......#....#OO.O.####O...###O...#.........###O..O
.#.O#.#O..#..#...#O..O..#..........#.......O..#.O...O.#..#O..O...O..#..O.............#.OO....O#..OO.
.....#.O.OO...#...O...O..........#......#..O.O....OO.#..#...O#O..#.....OO........O.#O.#.......OO#.OO
OO...#.O.......#O.O...O#.O....O.....OO.O.........##OO...OO...O.#..OO...O.#.O...O.O..O#OO.O#O..#..OO.
..O##.#..#...O..O.#....O.O##.O.#.O...O..#O.OO...O.#.....##O...O.O.......##O...OO..O#..O#.#......O.O.
.....O.....OO..O..O..O.#...O......O..OO..OO....OOO#.O..OO......#.O.....#O.O.O#....##OO..#O#.O..O#O.O
......O.O#...O..O.OO.O.OO.OOO...#O..O#...OO.#O.OO...O..#..O..O.#....O..OO....#......O.O.#O.##..O..O.
#.....#....O#O..O#O....O.......#.....O....#..#.OOOO#OOO#..#.OO....OO.O#.O......#..O.OO..O.#....O.O..
.O.O.#.#.O...#..#O.......##...OO..O...#......#.O#...O..O....#O.O.O.........#O.O#..O....##.O.O.......
....#..O.#.......#.#O..O..........#...#..O##..O#..O..OO.O###.#O#..O#O#O..#OO.#..O#.#.O..#....O.O....
...##...........O...#O.OOO..##O.O...#.OO.OO..O...O.....#.......#.....#........#....##.....O...#.#..O
.O......O.#...##O..#O..O......O#O....#.......O....#...O#....O.....#......#O..#.O..#.#.O.O#...O#.....
O..O.#........O.##.#..##....O.OO.......O.......O..#O#O......O...###.........OO...#.#..#........#.#..
O.........#..O.O...#O......#.O.#OO..O.##..O.#O.#..#..#.#.O.....#...#.....##....#.......O##...O#..O..
#OO..........O.O...#.OO....#...#.O#..OO#..#O.##.O....#O#..O....O..#...#.#....O.O...#.#O....OO.#.##..
.#...#O.#O#O###.OO.#..#....#OO.O....O.O#.O...........O#....O.#.O......#.O.#.#O.#..O.OO.....OO...OO.#
O#.........O....O.#....##.....O.....O.........#O.O#O...O.O#..O.#O....#.#...O....O#....##.......#....
.....OO#..O##..O.......O.#...#.OO.O.........#..O###...#.O..O#.O......O.....#.O.OO......#O...O#.....O
.O.O##.###OO..........O.......OOO..O.OO..##...#O..O...OO..#.O.....O.#..#.O.OO##.#.#...###....O...#..
.O..###...O...#.OOO#.O#.O#...O.#OO.OO...O..#.O......#.O.O.OO...#OO..#...#..O#O...O........##.OO.#...
.#..#O......#O......O#...#..#O...##O..#.O..O....O.#O..OO..O..#.#....O..O......O.O.#...##..O.O.#O....
.O.##.#...#O..#...O#.#.O..O#.......O....#.O.O.#.##.....#.......O.##..#.......O.....##.O.#.....#..#O.
...#.O.O.#O#.#...#...#OO.#O..O....O...O#....#.#.O..O..OO.#.OO..O...#O....O..#.......OO...O.....#.O..
O..O...O.......O.....##O#.O.#...OOO.O...........#..O..O.O.....O............#...........#...O.O..#.O.
..O.O.#O...O#.#.#O.OO.....##..O##O.O.O....#OOO...##.O.O.OO........O.#O........O.#.O.#.O.OO....O#.OO.
#.O.O##.....OO..#OO.O...O.#..#......O...OO....OO.#...O.##.O.OO.#.##..##O.O...#O#...##.....#..O#O.##.
..#OO..OO.##..#....O##.#O.OO##.O....#....O...O.........O....O#O.##.OOO.#..#......OO#..OO...#..#..#O.
.....#.#.O...O##....O.#O..O.#..#..O.#O.#O##..O.#..#O.#.O..O.......##......O#.##.O#..OO.....O#OOO.#..
O....O.O#.#...O.OO.........O...#...#...OO..##..OO..........#O.O.....#.#.OO.#..O#O.#...OO..O##.#.O...
..#....##..............O..#.#..OO.OOO..#OO.O#O.OO#..#...O.#...O..O...OO......#.O..#....O.OO.O....##.
O.#O##....#.OO....#.#...#.....O......O......#.#......#OO.....###...#...#..O...O...O.OO.#...#.......#
....O..#....#....O...#...O....OO.O##..#.O..OO.#.#.#......#O.OO......O##O.#O...#.#.....O....#O..O....
#OO.#..O......#.....#........#...#.....O...OOO.......OO##O....#......O.O...O##.O.OOO.#........O.#...
O.OO.......O..OO.O.OO.OO..OO#...##.#.....#...O.#.O....O...#.OO.##.#.....OO..O#......#OOOO....O....##
...#...#..#....#.....O..O#O..#.##O.O......O.#O......O..##...#O#O..##..O.#....O.#...O.OO...#O#....OOO
.........OOOO.O.O.O...#........#....OO.#OO#....#O........#.....#O.....##O.....#O..O.O...#...#....OO."""

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


# data = get_data(day=14, year=2023)

# part_1(data)
part_2(data)
