import regex as re
import matplotlib.pyplot as plt
from functools import reduce
from operator import mul

input_file = "input.txt"
with open(input_file, "r") as f:
    lines = f.readlines()

pattern = re.compile(r"[-]{0,1}\d+")
robots = []
for line in lines:
    match = pattern.findall(line)
    start = (int(match[0]), int(match[1]))
    vector = (int(match[2]), int(match[3]))
    robots.append((start, vector))


def run_simulation(robots, seconds, width, height):
    for i, robot in enumerate(robots):
        start, vector = robot
        x, y = start
        dx, dy = vector
        x = (x + dx * seconds) % width
        y = (y + dy * seconds) % height
        robots[i] = ((x, y), vector)

    return robots


def count_by_quadrant(robots, width, height):
    quadrants = [0, 0, 0, 0]
    mid_x = width // 2
    mid_y = height // 2
    for robot in robots:
        x, y = robot[0]
        if x < mid_x and y < mid_y:
            quadrants[0] += 1
        elif x > mid_x and y < mid_y:
            quadrants[1] += 1
        elif x < mid_x and y > mid_y:
            quadrants[2] += 1
        elif x > mid_x and y > mid_y:
            quadrants[3] += 1

    return quadrants


def count_score(robots, width, height):
    return reduce(mul, count_by_quadrant(robots, width, height))


WIDTH = 101
TALL = 103


def part_one():
    grid = robots.copy()
    run_simulation(grid, 100, WIDTH, TALL)
    return count_score(grid, WIDTH, TALL)


print(f"Part One: {part_one()}")


def part_two():
    grid = robots.copy()
    min_score = count_score(grid, WIDTH, TALL)
    min_score_index = 0
    for i in range(1, 10000):
        run_simulation(grid, 1, WIDTH, TALL)
        current_score = count_score(grid, WIDTH, TALL)
        if current_score < min_score:
            min_score = current_score
            min_score_index = i

    grid = robots.copy()
    run_simulation(grid, min_score_index, WIDTH, TALL)

    map = [[0 for _ in range(WIDTH)] for _ in range(TALL)]
    for robot in grid:
        x, y = robot[0]
        map[y][x] = 1

    plt.imshow(map, vmin=0, vmax=1)
    plt.axis("off")
    plt.show()

    return min_score_index


print(f"Part Two: {part_two()}")
