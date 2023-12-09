import re

import numpy as np
from aocd import get_data, submit
from tqdm import tqdm


def parse_data(data):
    maps = []

    data_split = data.split("\n\n")
    seeds = data_split[0]
    seeds = [int(x) for x in re.findall(r"\d+", seeds)]

    for line in data_split[1:]:
        map_lines = []
        map_name, rest = line.split(" map:")
        for line_2 in rest.split("\n")[1:]:
            map_lines.append(tuple([int(x) for x in re.findall(r"\d+", line_2)]))
        maps.append(map_lines)

    return seeds, maps


def perform_mapping_part_1(seed, maps):
    val = seed

    for mapping in maps:
        mapped = False
        for dst, src, size in mapping:
            if src <= val < src + size:
                off = val - src
                new_val = dst + off
                mapped = True

        if not mapped:
            new_val = val

        val = new_val

    return val


def part_1(data):
    seeds, maps = parse_data(data)

    seed_to_destination = [perform_mapping_part_1(seed, maps) for seed in seeds]

    solution = min(seed_to_destination)

    submit(solution, part="a", day=5, year=2023)


def perform_mapping_part_2(R, mapping):
    A = []

    for dest, src, size in mapping:
        src_end = src + size
        NR = []

        while R:
            start, end = R.pop()
            before = (start, min(end, src))
            inter = (max(start, src), min(end, src_end))
            after = (max(start, src_end), end)

            if before[1] > before[0]:
                NR.append(before)
            if inter[1] > inter[0]:
                A.append((inter[0] - src + dest, inter[1] - src + dest))
            if after[1] > after[0]:
                NR.append(after)

        R = NR

    return A + R


def part_2(data):
    seeds, maps = parse_data(data)
    print("*" * 25)
    for map in maps:
        print(map)

    solution = 99999999

    for seed_range in list(zip(seeds[::2], seeds[1::2])):
        # [x, y)
        seed_range = [(seed_range[0], seed_range[0] + seed_range[1])]
        for map in maps:
            seed_range = perform_mapping_part_2(seed_range, map)

        solution = min(solution, min(seed_range)[0])

    print(solution)
    submit(solution, part="b", day=5, year=2023)


data = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

groups = data.split("\n\n")

for g in groups[1:]:
    step_mapping = [tuple(map(int, l.split())) for l in g.splitlines()[1:]]

    print(step_mapping)

# data = get_data(day=5, year=2023)

# part_1(data)
part_2(data)
