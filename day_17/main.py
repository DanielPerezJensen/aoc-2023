from itertools import count
from queue import PriorityQueue

import numpy as np
from aocd import get_data, submit


def parse_data(data):
    city_map = {
        complex(x, y): loss
        for y, l in enumerate(data.splitlines())
        for x, loss in enumerate(map(int, l.strip()))
    }

    return city_map, max(city_map, key=abs)


NORTH = 0 - 1j
EAST = 1 + 0j
SOUTH = 0 + 1j
WEST = -1 + 0j


def search(city_map, min_run, max_run, end_point):
    unique = count()
    # a star with priority queue

    # (hypothesis, heat loss on the path, current straight run, current direction, current position)
    paths = PriorityQueue()
    h = int(abs(end_point))

    paths.put((h, 0, 1, next(unique), EAST, 0 + 0j))
    paths.put((h, 0, 1, next(unique), SOUTH, 0 + 0j))

    history = set()

    while not paths.empty():
        _, heat_loss, run_len, _, dir, pos = paths.get()
        hist = (run_len, dir, pos)
        if hist in history:
            # We've seen a shorter path through here
            continue
        history.add(hist)
        if pos == end_point and run_len > min_run:
            # Found the path!
            return heat_loss
        pos += dir
        if pos in city_map:
            heat_loss += city_map[pos]
            h = int(abs(end_point - pos)) + heat_loss
            # Turn left and right
            if run_len >= min_run:
                paths.put((h, heat_loss, 1, next(unique), dir * 1j, pos))
                paths.put((h, heat_loss, 1, next(unique), dir * -1j, pos))
            # Go straight
            if run_len < max_run:
                paths.put((h, heat_loss, run_len + 1, next(unique), dir, pos))


def part_1(data):
    city_map, goal = parse_data(data)

    solution = search(city_map, 0, 3, goal)

    print(solution)

    submit(solution, part="a", day=17, year=2023)


def part_2(data):
    city_map, goal = parse_data(data)

    solution = search(city_map, 4, 10, goal)

    print(solution)
    submit(solution, part="b", day=17, year=2023)


data = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""


# data = get_data(day=17, year=2023)

part_1(data)
part_2(data)
