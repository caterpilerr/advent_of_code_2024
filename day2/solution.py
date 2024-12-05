from typing import List

input_file = 'input.txt'
with open(input_file, 'r') as f:
    lines = f.readlines()

input = [[int(item) for item in line.split()] for line in lines]

MIN_DIF = 1
MAX_DIF = 3

def is_save(record: List[int]) -> bool:
    """Check if a sequence is valid based on MIN_DIF, MAX_DIF, and monotonicity."""
    n = len(record)
    if n < 2:
        return True

    start_sign = record[1] > record[0]
    for i in range(1, n):
        delta = abs(record[i] - record[i - 1])
        if delta < MIN_DIF or delta > MAX_DIF:
            return False

        current_sign = record[i] > record[i - 1]
        if current_sign != start_sign:
            return False

    return True

def is_save_with_removal(data: List[int]) -> bool:
    """
    Check if a sequence can be valid with at most one removal.
    A sequence is valid if it satisfies the conditions or becomes valid by removing one element.
    """
    def is_valid_with_removal(index: int) -> bool:
        """Check if the sequence is valid after removing the element at `index`."""
        filtered = data[:index] + data[index + 1:]
        return is_save(filtered)

    n = len(data)
    if n < 2:
        return True

    prev_sign = data[1] >= data[0]
    for i in range(1, n):
        delta = data[i] - data[i - 1]
        abs_delta = abs(delta)
        current_sign = delta >= 0

        if abs_delta < MIN_DIF or abs_delta > MAX_DIF or current_sign != prev_sign:
            if i == 2 and is_valid_with_removal(0):
                return True
                
            return is_valid_with_removal(i) or is_valid_with_removal(i - 1)

        prev_sign = current_sign

    return True

def part_one():
    return sum([is_save(item) for item in input])

print(f'Part One: {part_one()}')

def part_two():
    return sum([is_save_with_removal(item) for item in input])

print(f'Part Two: {part_two()}')
