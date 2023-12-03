import re

import numpy as np
from aocd import get_data, submit


def parse_data(data):
    grid = np.array([re.findall(r".", line) for line in data.split("\n")])

    numbers_dict = {}
    numbers_id = {}
    curr_id = 0

    x, y = 0, 0

    while x < grid.shape[0]:
        while y < grid.shape[1]:
            value = grid[x, y]

            coords = []
            number = ""

            if re.match(r"[1-9]", value):
                while y < grid.shape[1] and re.match(r"[0-9]", grid[x, y]):
                    number += grid[x, y]
                    coords += ((x, y),)
                    y += 1

                for coord in coords:
                    numbers_dict[coord] = int(number)
                    numbers_id[(int(number), coord)] = curr_id

                curr_id += 1

            y += 1

        y = 0
        x += 1

    return grid, numbers_dict, numbers_id


def find_neighbours(grid_shape, x, y):
    pn = [
        (x - 1, y),
        (x + 1, y),
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    ]

    max_x, max_y = grid_shape

    neighbours = [
        neighbour
        for neighbour in pn
        if validate_cell(max_x, max_y, neighbour) and neighbour != (x, y)
    ]

    return neighbours


def validate_cell(max_x, max_y, coordinate):
    if coordinate[0] < 0 or coordinate[1] < 0:
        return False
    elif coordinate[0] >= max_x or coordinate[1] >= max_y:
        return False
    else:
        return True


def part_1(data):
    solution = 0
    grid, numbers_dict, numbers_id = parse_data(data)
    seen = set()

    for x, y in np.ndindex(grid.shape):
        value = grid[x, y]

        if value in ".\r\n0123456789":
            continue

        neighbours = find_neighbours(grid.shape, x, y)

        for neighbour in neighbours:
            if neighbour in numbers_dict:
                number = numbers_dict[neighbour]
                if numbers_id[(number, neighbour)] not in seen:
                    seen.add(numbers_id[(number, neighbour)])
                    solution += number

    print(solution)
    submit(solution, part="a", day=3, year=2023)


def part_2(data):
    solution = 0
    grid, numbers_dict, numbers_id = parse_data(data)
    seen = set()

    count_lol = []

    for x, y in np.ndindex(grid.shape):
        value = grid[x, y]

        if not value == "*":
            continue

        neighbours = find_neighbours(grid.shape, x, y)

        count_list = []

        for neighbour in neighbours:
            if neighbour in numbers_dict:
                number = numbers_dict[neighbour]

                if numbers_id[(number, neighbour)] not in seen:
                    seen.add(numbers_id[(number, neighbour)])
                    count_list.append(number)

        if len(count_list) == 2:
            count_lol.append(count_list)

    for count_list in count_lol:
        solution += np.prod(count_list)

    print(solution)
    submit(solution, part="b", day=3, year=2023)


data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


data = get_data(day=3, year=2023)

part_1(data)
part_2(data)
