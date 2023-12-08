import math
import re

import networkx as nx
import numpy as np
from aocd import get_data, submit
from tqdm import tqdm


def parse_data(data):
    data = data.splitlines()

    route = data[0]

    directions = {}

    for line in data[2:]:
        source, destinations = line.split(" = ")

        left, right = destinations.split(",")
        left = re.findall(r"[A-Z]+", left)[0]
        right = re.findall(r"[A-Z]+", right)[0]

        directions[source] = (left, right)

    return route, directions


def part_1(data):
    route, directions = parse_data(data)

    curr_place = "AAA"

    solution = 0

    while curr_place != "ZZZ":
        for r in route:
            if r == "L":
                curr_place = directions[curr_place][0]
            if r == "R":
                curr_place = directions[curr_place][1]

            solution += 1

    print(solution)
    submit(solution, part="a", day=8, year=2023)


def parse_data2(data):
    data = data.splitlines()

    route = data[0]

    directions = {}
    starts = []

    for line in data[2:]:
        source, destinations = line.split(" = ")

        if source[2] == "A":
            starts.append(source)

        left, right = destinations.split(",")
        left = re.findall(r"[A-Z1-9]+", left)[0]
        right = re.findall(r"[A-Z1-9]+", right)[0]

        directions[source] = (left, right)

    return route, directions, starts


class Ghost:
    def __init__(self, start):
        self.curr_place = start

    def step(self, r, directions):
        if r == "L":
            self.curr_place = directions[self.curr_place][0]
        if r == "R":
            self.curr_place = directions[self.curr_place][1]

    def done(self):
        return self.curr_place[2] == "Z"


def part_2(data):
    route, directions, starts = parse_data2(data)

    solution = 0

    ghosts = []

    for start in starts:
        ghosts.append(Ghost(start))

    multiples = []

    for ghost in ghosts:
        steps = 0
        while not ghost.done():
            for r in route:
                ghost.step(r, directions)
                steps += 1
                if ghost.done():
                    multiples.append(steps)
                    break

    solution = np.lcm.reduce(multiples)

    print(solution)
    submit(solution, part="b", day=8, year=2023)


data = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

data2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

data3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

data = get_data(day=8, year=2023)

part_1(data)
part_2(data)
