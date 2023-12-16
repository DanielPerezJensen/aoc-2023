import re

import numpy as np
from aocd import get_data, submit
from tqdm import tqdm


def parse_data(data):
    map = [line for line in data.splitlines()]

    return map


direction_map = {"right": (0, 1), "left": (0, -1), "up": (-1, 0), "down": (1, 0)}

move_map = {
    "/": {"right": ("up",), "left": ("down",), "up": ("right",), "down": ("left",)},
    "\\": {"right": ("down",), "left": ("up",), "up": ("left",), "down": ("right",)},
    ".": {"right": ("right",), "left": ("left",), "up": ("up",), "down": ("down",)},
    "|": {
        "down": ("down",),
        "up": ("up",),
        "left": ("up", "down"),
        "right": ("up", "down"),
    },
    "-": {
        "down": ("left", "right"),
        "up": ("left", "right"),
        "left": ("left",),
        "right": ("right",),
    },
}


class Light:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def get_move(self, map):
        return move_map[map[self.x][self.y]][self.direction]

    def done(self, map, seen_paths):
        if self.x < 0 or self.y < 0:
            return True
        elif self.x >= len(map) or self.y >= len(map[0]):
            return True
        elif (self.x, self.y, self.direction) in seen_paths:
            return True
        else:
            return False

    def move(self, map):
        moves = self.get_move(map)

        if len(moves) > 1:
            new_x_diff, new_y_diff = direction_map[moves[1]]
            new_light = Light(self.x + new_x_diff, self.y + new_y_diff, moves[1])

            x_diff, y_diff = direction_map[moves[0]]
            self.x += x_diff
            self.y += y_diff
            self.direction = moves[0]

            return new_light

        else:
            x_diff, y_diff = direction_map[moves[0]]
            self.x += x_diff
            self.y += y_diff
            self.direction = moves[0]


def find_energized(map, lights):
    energised = set()
    seen_paths = set()

    for light in lights:
        energised.add((light.x, light.y))

    while not all([light.done(map, seen_paths) for light in lights]):
        for light in lights:
            if light.done(map, seen_paths):
                continue
            energised.add((light.x, light.y))
            seen_paths.add((light.x, light.y, light.direction))
            poss_new_light = light.move(map)

            if poss_new_light is not None:
                lights.append(poss_new_light)

    solution = len(set(energised))

    return solution


def part_1(data, start_pos=(0, 0)):
    map = parse_data(data)
    light = Light(start_pos[0], start_pos[1], "right")

    lights = [light]

    solution = find_energized(map, lights)

    print(solution)
    submit(solution, part="a", day=16, year=2023)

    return solution


def part_2(data):
    map = parse_data(data)

    combinations = [
        (0, 0, ["down"]),
        (0, 0, ["right"]),
        (0, len(map) - 1, ["down"]),
        (0, len(map) - 1, ["left"]),
        (len(map) - 1, 0, ["up", "right"]),
        (len(map) - 1, 0, ["right"]),
        (len(map) - 1, len(map[0]) - 1, ["up"]),
        (len(map) - 1, len(map[0]) - 1, ["left"]),
    ]

    for i in range(1, len(map[0]) - 1):
        combinations.append((0, i, ["down"]))
        combinations.append((len(map) - 1, i, ["up"]))

    for i in range(1, len(map) - 1):
        combinations.append((i, 0, ["right"]))
        combinations.append((i, len(map[0]) - 1, ["left"]))

    solutions = []
    for comb in tqdm(combinations):
        lights = [Light(comb[0], comb[1], direction) for direction in comb[2]]
        solutions.append(find_energized(map, lights))

    solution = max(solutions)
    print(solution)

    submit(solution, part="b", day=16, year=2023)


data = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


data = get_data(day=16, year=2023)

part_1(data)
part_2(data)
