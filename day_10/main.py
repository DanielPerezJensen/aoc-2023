import re
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from aocd import get_data, submit

pipe_to_direction_mappings = {
    "|": ["n", "s"],
    "-": ["w", "e"],
    "L": ["n", "e"],
    "J": ["n", "w"],
    "7": ["s", "w"],
    "F": ["s", "e"],
    "S": ["n", "s", "w", "e"],
}

directions_mapping = {
    "n": (0, -1, "s"),
    "s": (0, 1, "n"),
    "w": (-1, 0, "e"),
    "e": (1, 0, "w"),
}


def pipe_to_direction(con):
    """
    Maps a pipe to the directions.
    """
    possible_directions = pipe_to_direction_mappings[con]

    return [directions_mapping[pd][:2] for pd in possible_directions]


def find_starting_point(lines):
    """
    Finds the starting point of the maze.
    """
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            if character == "S":
                return x, y


def create_graph(data):
    lines = data.splitlines()
    starting_point = find_starting_point(lines)
    connections = {(starting_point): []}

    # Find all the connections.
    for y, line in enumerate(lines):
        for x, con in enumerate(line):
            moves = []
            if con not in pipe_to_direction_mappings:
                continue

            possible_directions = pipe_to_direction(con)
            moves = [(pd[0] + x, pd[1] + y) for pd in possible_directions]

            for move in moves:
                if starting_point == move:
                    connections[starting_point].append((x, y))

            if starting_point != (x, y):
                connections[(x, y)] = moves

    return connections, starting_point


def part_1(data):
    connections, starting_point = create_graph(data)
    dist = {(starting_point): 0}
    queue = deque([starting_point])

    # BFS - Breadth First Search
    while queue:
        current = queue.popleft()
        for con in connections[current]:
            if con not in dist:
                dist[con] = dist[current] + 1
                queue.append(con)

    solution = max(dist.values())
    submit(solution, part="a", day=10, year=2023)


def part_2(data):
    connections, starting_point = create_graph(data)

    dist = {(starting_point): 0}
    queue = deque([starting_point])

    # BFS - Breadth First Search
    while queue:
        current = queue.popleft()
        for con in connections[current]:
            if con not in dist:
                dist[con] = dist[current] + 1
                queue.append(con)

    solution = 0

    for y, line in enumerate(data.splitlines()):
        new_line = []
        for x, value in enumerate(line):
            value = value if (x, y) in dist else "."
            new_line.append(value)

        new_line_string = "".join(new_line)

        new_line_string = re.sub(r"L-*7", "|", new_line_string)
        new_line_string = re.sub(r"L-*J", "||", new_line_string)
        new_line_string = re.sub(r"F-*7", "||", new_line_string)
        new_line_string = re.sub(r"F-*J", "|", new_line_string)

        inside = False
        inside_cells = 0

        for c in new_line_string:
            if c == "." and inside:
                inside_cells += 1
            elif c in "F7LJ|S":
                inside = not inside

        solution += inside_cells

    print(solution)
    submit(solution, part="b", day=10, year=2023)


data = """.....
.S-7.
.|.|.
.L-J.
....."""

data1 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

data3 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

data4 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

data5 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""


data = get_data(day=10, year=2023)

part_1(data)
part_2(data)
