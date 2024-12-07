input_file = "input.txt"
with open(input_file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

rows = len(lines)
cols = len(lines[0])


def check_match(x: int, y: int, direction: tuple[int, int], pattern: str) -> bool:
    """Check if the pattern matches starting from (x, y) in the given direction."""
    dx, dy = direction
    for char in pattern:
        if x < 0 or x >= rows or y < 0 or y >= cols or lines[x][y] != char:
            return False
        x += dx
        y += dy
    return True


def check_match_both(x: int, y: int, direction: tuple[int, int], pattern: str) -> bool:
    """Check if the pattern or its reverse matches in the given direction."""
    return check_match(x, y, direction, pattern) or check_match(
        x, y, direction, pattern[::-1]
    )


def check_xmas(x: int, y: int) -> bool:
    """Check for the specific 'XMAS' pattern structure."""
    dir1, dir2 = (1, 1), (-1, 1)  # Diagonal directions
    return check_match_both(x, y, dir1, "MAS") and check_match_both(
        x + 2, y, dir2, "MAS"
    )


def part_one() -> int:
    """Count all occurrences of the pattern in any direction."""
    matches = 0
    directions = [
        (0, 1),  # Right
        (1, 0),  # Down
        (0, -1),  # Left
        (-1, 0),  # Up
        (1, 1),  # Down-Right
        (1, -1),  # Down-Left
        (-1, 1),  # Up-Right
        (-1, -1),  # Up-Left
    ]
    for i in range(rows):
        for j in range(cols):
            for direction in directions:
                if check_match(i, j, direction, "XMAS"):
                    matches += 1
    return matches


print(f"Part One: {part_one()}")


def part_two() -> int:
    """Count X-MAS pattern structures."""
    matches = 0
    for i in range(rows):
        for j in range(cols):
            if check_xmas(i, j):
                matches += 1
    return matches


print(f"Part Two: {part_two()}")
