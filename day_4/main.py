import re

import numpy as np
from aocd import get_data, submit


def parse_data(data):
    games = []

    for line in data.splitlines():
        left_side, right_side = line.split("|")
        card_side, numbers_side = left_side.split(":")
        card_number = int(re.findall(r"\d+", card_side)[0])
        numbers = [int(x) for x in numbers_side.split()]
        winning_numbers = [int(x) for x in right_side.split()]

        games.append((card_number, numbers, winning_numbers))

    return games


def get_winning_numbers(games):
    winning_numbers_games = np.ones(len(games), dtype=int)

    for i, game in enumerate(games):
        card_number, numbers, winning_numbers = game
        numbers = set(numbers)
        winning_numbers = set(winning_numbers)

        winning_amount = len(numbers.intersection(winning_numbers))

        winning_numbers_games[i] = int(winning_amount)

    return winning_numbers_games


def part_1(data):
    games = parse_data(data)

    solution = 0

    for i, game in enumerate(games):
        card_number, numbers, winning_numbers = game
        numbers = set(numbers)
        winning_numbers = set(winning_numbers)

        winning_amount = len(numbers.intersection(winning_numbers))

        if winning_amount == 0:
            points = 0
        else:
            points = 2 ** (winning_amount - 1)

        solution += points

    print(solution)
    submit(solution, part="a", day=4, year=2023)


def part_2(data):
    games = parse_data(data)

    winning_numbers = get_winning_numbers(games)
    card_counts = np.ones(winning_numbers.shape, dtype=int)

    for i, item in enumerate(winning_numbers):
        card_count = card_counts[i]
        winning_amount = winning_numbers[i]
        added_cards = winning_amount * card_count

        card_counts[i + 1 : winning_amount + i + 1] += added_cards // winning_amount

    solution = int(np.sum(card_counts))
    print(solution)
    submit(solution, part="b", day=4, year=2023)


data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


data = get_data(day=4, year=2023)

part_1(data)
part_2(data)
