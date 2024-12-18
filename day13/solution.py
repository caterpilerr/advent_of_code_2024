import regex as re
import numpy as np


input_file = "input.txt"
with open(input_file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

programs = []
pattern = re.compile(r"(\d+)")
for i in range(0, len(lines), 4):
    x_a, y_a = map(int, re.findall(pattern, lines[i]))
    x_b, y_b = map(int, re.findall(pattern, lines[i + 1]))
    x_prize, y_prize = map(int, re.findall(pattern, lines[i + 2]))
    programs.append(((x_a, y_a), (x_b, y_b), (x_prize, y_prize)))


def solve_linear_system(xp, yp, ax, ay, bx, by):
    # Coefficients matrix
    A = np.array([[ax, bx], [ay, by]])
    # Constants vector
    B = np.array([xp, yp])

    # Solve the system
    try:
        c = np.linalg.solve(A, B)
        c1 = int(np.rint(c[0]))
        c2 = int(np.rint(c[1]))
        if c1 * ax + c2 * bx != xp or c1 * ay + c2 * by != yp:
            return None
        return c1, c2
    except np.linalg.LinAlgError:
        return None


def part_one():
    result = 0
    for a, b, prize in programs:
        sol = solve_linear_system(*prize, *a, *b)
        if sol is None:
            continue
        c1, c2 = sol
        if c1 > 100 or c2 > 100:
            continue
        result += c1 * 3 + c2

    return result


print(f"Part One: {part_one()}")


def part_two():
    result = 0
    for a, b, prize in programs:
        sol = solve_linear_system(*prize, *a, *b)
        final_prize = (10000000000000 + prize[0], 10000000000000 + prize[1])
        sol = solve_linear_system(*final_prize, *a, *b)
        if sol is None:
            continue
        c1, c2 = sol
        result += c1 * 3 + c2

    return result


print(f"Part Two: {part_two()}")
