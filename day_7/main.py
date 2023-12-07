import re
from functools import cmp_to_key

import numpy as np
from aocd import get_data, submit


def parse_data(data):
    data = data.splitlines()

    hands = []
    bets = []

    for line in data:
        left, right = line.split(" ")
        hands.append(left)
        bets.append(int(right))

    return hands, bets


def count_hand(hand, cards):
    counts = np.zeros(len(cards))

    for card in hand:
        counts[cards.index(card)] += 1

    return counts


def sort_hand(counts):
    if 5 in counts:
        return 7
    if 4 in counts:
        return 6
    if (3 in counts) and (2 in counts):
        return 5
    if 3 in counts:
        return 4
    if len([x for x in counts if x == 2]) == 2:
        return 3
    if 2 in counts:
        return 2
    return 1


def compare_hand(hand1, hand2):
    cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

    count1 = count_hand(hand1, cards)
    count2 = count_hand(hand2, cards)

    count1_value = sort_hand(count1)
    count2_value = sort_hand(count2)

    if count1_value > count2_value:
        return 1
    if count1_value < count2_value:
        return -1
    else:
        for h1, h2 in zip(hand1, hand2):
            if cards.index(h1) > cards.index(h2):
                return -1
            if cards.index(h1) < cards.index(h2):
                return 1


def part_1(data):
    hands, bets = parse_data(data)

    sorted_list = sorted(
        list(zip(hands, bets)),
        key=cmp_to_key(lambda hand1, hand2: compare_hand(hand1[0], hand2[0])),
    )

    solution = 0

    for i, item in enumerate(sorted_list):
        solution += item[1] * (i + 1)

    print(solution)

    # submit(solution, part="a", day=4, year=2023)


def compare_hand2(hand1, hand2):
    cards = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

    count1 = count_hand(hand1, cards)
    count2 = count_hand(hand2, cards)

    # Since simply setting the joker card to the highest current card is the most effective
    # we can just add the number of jokers to the count ranking

    count1_jokers = count1[-1]
    count1[-1] = 0
    count2_jokers = count2[-1]
    count2[-1] = 0

    count1[count1.argmax()] += count1_jokers
    count2[count2.argmax()] += count2_jokers

    count1_value = sort_hand(count1)
    count2_value = sort_hand(count2)

    if count1_value > count2_value:
        return 1
    if count1_value < count2_value:
        return -1
    else:
        for h1, h2 in zip(hand1, hand2):
            if cards.index(h1) > cards.index(h2):
                return -1
            if cards.index(h1) < cards.index(h2):
                return 1


def part_2(data):
    hands, bets = parse_data(data)

    sorted_list = sorted(
        list(zip(hands, bets)),
        key=cmp_to_key(lambda hand1, hand2: compare_hand2(hand1[0], hand2[0])),
    )

    solution = 0

    for i, item in enumerate(sorted_list):
        solution += item[1] * (i + 1)

    print(solution)

    submit(solution, part="b", day=4, year=2023)


data = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


data = get_data(day=6, year=2023)

part_1(data)
part_2(data)
