import re

import numpy as np
from aocd import get_data, submit


def order_game(game):
    game = sorted(game, key=lambda x: x.split(" ")[1])

    return game


def parse_data(data):
    games = []

    for line in data.splitlines():
        game_idx, game_data = line.split(":")
        game_data = re.split(r"[,;]+", game_data)
        game_data = [g.strip() for g in game_data]

        game_draws = []

        for draw in game_data:
            number, colour = draw.split(" ")
            game_draws.append((colour, int(number)))

        games.append(game_draws)

    return games


def valid_game(draws):
    bag_count = {"red": 12, "green": 13, "blue": 14}

    for colour, draw in draws:
        if bag_count[colour] < draw:
            return 0
    return 1


def part_1(data):
    games = parse_data(data)

    solution = 0

    for i, game in enumerate(games):
        if valid_game(game):
            solution += i + 1

    print(solution)
    submit(solution, part="a", day=2, year=2023)


def part_2(data):
    games = parse_data(data)

    solution = 0

    for game in games:
        # rgb
        max_count = [0, 0, 0]
        for colour, draw in game:
            if colour == "red":
                max_count[0] = max(max_count[0], draw)
            elif colour == "green":
                max_count[1] = max(max_count[1], draw)
            elif colour == "blue":
                max_count[2] = max(max_count[2], draw)

        solution += np.prod(max_count)

    print(solution)
    submit(solution, part="b", day=2, year=2023)


data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

data = get_data(day=2, year=2023)

part_1(data)
part_2(data)
