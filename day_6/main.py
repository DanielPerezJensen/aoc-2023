import re

import numpy as np
from aocd import get_data, submit


def play_game(times, distances):
    wins = []

    for time, distance in zip(times, distances):
        curr_speed = 1
        won = 0
        for i in range(1, time):
            remaining_time = time - curr_speed
            if remaining_time * curr_speed > distance:
                won += 1
            curr_speed += 1

        wins.append(won)

    return int(np.prod(wins))


def part_1(data):
    time_line, distance_line = data.splitlines()

    times = [int(x) for x in re.findall(r"\d+", time_line)]
    distances = [int(x) for x in re.findall(r"\d+", distance_line)]
    solution = play_game(times, distances)

    print(solution)

    submit(solution, part="a", day=6, year=2023)


def part_2(data):
    time_line, distance_line = data.splitlines()

    times = [x for x in re.findall(r"\d+", time_line)]
    distances = [x for x in re.findall(r"\d+", distance_line)]

    times = [int("".join(times))]
    distances = [int("".join(distances))]

    solution = play_game(times, distances)

    print(solution)

    submit(solution, part="b", day=6, year=2023)


data = """Time:        54     70     82     75
Distance:   239   1142   1295   1253"""


data = get_data(day=6, year=2023)

part_1(data)
part_2(data)
