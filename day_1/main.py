import re

from aocd import get_data, submit


def part_1(data):
    data = data.splitlines()

    sum = 0

    for d in data:
        ints = re.findall(r"\d", d)

        first_int = ints[0]
        second_int = ints[-1]

        number = first_int + second_int

        sum += int(number)

    submit(sum, part="a", day=1, year=2023)


def part_2(data):
    digit_strings = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    sum = 0

    for line in data.splitlines():
        for digit_string, digit in digit_strings.items():
            line = line.replace(digit_string, str(digit) + digit_string[-1])

        digits = re.findall(r"\d", line)

        first_int = digits[0]
        second_int = digits[-1]

        number = first_int + second_int

        sum += int(number)

    submit(sum, part="b", day=1, year=2023)


data = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

data = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

data = get_data(day=1, year=2023)

part_1(data)
part_2(data)
