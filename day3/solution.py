import re
from typing import Tuple

input_file = "input.txt"
with open(input_file, "r") as f:
    lines = f.readlines()

input = "".join(lines)

# Regular expressions
CORRECT_PATTERN = re.compile(r"mul\(\d{1,3},\d{1,3}\)")
FULL_PATTERN = re.compile(r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\))")
NUMBERS_PATTERN = re.compile(r"\d{1,3}")


def extract_numbers(expression: str) -> Tuple[int, int]:
    """
    Extracts two numbers from the given string.
    """
    numbers = NUMBERS_PATTERN.findall(expression)
    if len(numbers) != 2:
        raise ValueError(f"Expected two numbers, found: {numbers}")
    return int(numbers[0]), int(numbers[1])


def part_one() -> int:
    """
    Computes the result for Part One by summing the products of all valid 'mul' expressions.
    """
    result = 0
    for match in CORRECT_PATTERN.findall(input):
        a, b = extract_numbers(match)
        result += a * b
    return result


print(f"Part One: {part_one()}")


def part_two() -> int:
    """
    Computes the result for Part Two by conditionally summing 'mul' results based on 'do()' and 'don't()' directives.
    """
    do_execute = True
    result = 0
    for match in FULL_PATTERN.findall(input):
        if match == "do()":
            do_execute = True
        elif match == "don't()":
            do_execute = False
        elif "mul" in match and do_execute:
            a, b = extract_numbers(match)
            result += a * b
    return result


print(f"Part Two: {part_two()}")
