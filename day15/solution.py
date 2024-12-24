from collections import deque

input_file = "input.txt"
with open(input_file, "r") as f:
    lines = f.readlines()

grid = []
commands = []
current = grid
for line in lines:
    if line == "\n":
        current = commands
        continue

    current.append(list(line.strip()))


command_line = [char for line in commands for char in line]


def find_robot(grid):
    for x, line in enumerate(grid):
        for y, char in enumerate(line):
            if char == "@":
                return (x, y)

    raise ValueError("Robot not found")


DIRECTIONS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}


def apply_command(command, grid, robot):
    vector = DIRECTIONS[command]
    moving_group = list()
    current = robot
    while True:
        x, y = current
        if grid[x][y] == "#":
            return

        if grid[x][y] == ".":
            break

        moving_group.append(current)
        current = (current[0] + vector[0], current[1] + vector[1])

    for x, y in reversed(moving_group):
        temp = grid[x + vector[0]][y + vector[1]]
        grid[x + vector[0]][y + vector[1]] = grid[x][y]
        grid[x][y] = temp

    robot = (robot[0] + vector[0], robot[1] + vector[1])


def apply_command2(command, grid, robot, items_cells):
    vector = DIRECTIONS[command]
    moving_group = set()
    queue = deque()
    queue.append((robot,))
    visited = set()
    while queue:
        item = queue.popleft()
        if item in visited:
            continue
        visited.add(item)

        for cell in item:
            x, y = cell
            next_cell = (x + vector[0], y + vector[1])
            if next_cell in item:
                continue

            if grid[next_cell[0]][next_cell[1]] == "#":
                return robot

            if not next_cell in items_cells:
                continue

            next_item = items_cells[next_cell]
            queue.append(next_item)

        moving_group.add(item)

    for item in moving_group:
        for x, y in item:
            grid[x][y] = "."
            items_cells.pop((x, y))

    for item in moving_group:
        if len(item) == 1:
            next_x, next_y = item[0][0] + vector[0], item[0][1] + vector[1]
            grid[next_x][next_y] = "@"
            items_cells[(next_x, next_y)] = ((next_x, next_y),)
            robot = (next_x, next_y)
        else:
            left = item[0]
            right = item[1]
            next_left_x, next_left_y = left[0] + vector[0], left[1] + vector[1]
            next_right_x, next_right_y = right[0] + vector[0], right[1] + vector[1]
            grid[next_left_x][next_left_y] = "["
            grid[next_right_x][next_right_y] = "]"
            items_cells[(next_left_x, next_left_y)] = (next_left_x, next_left_y), (
                next_right_x,
                next_right_y,
            )
            items_cells[(next_right_x, next_right_y)] = (next_left_x, next_left_y), (
                next_right_x,
                next_right_y,
            )

    return robot


def part_one():
    grid_one = [list(line) for line in grid]
    robot = find_robot(grid_one)
    for command in command_line:
        apply_command(command, grid_one, robot)

    return count_score(grid_one)


def count_score(grid):
    result = 0
    for x, line in enumerate(grid):
        for y, char in enumerate(line):
            if char == "O" or char == "[":
                result += 100 * x + y

    return result


print(f"Part One: {part_one()}")


def part_two():
    items = {}
    grid2 = []
    # f the tile is #, the new map contains ## instead.
    # If the tile is O, the new map contains [] instead.
    # If the tile is ., the new map contains .. instead.
    # If the tile is @, the new map contains @. instead.
    for line in grid:
        row = []
        for char in line:
            if char == "#":
                row.extend("##")
            elif char == "O":
                row.extend("[]")
                items[(len(grid2), len(row) - 2)] = (len(grid2), len(row) - 2), (
                    len(grid2),
                    len(row) - 1,
                )
                items[(len(grid2), len(row) - 1)] = items[(len(grid2), len(row) - 2)]
            elif char == ".":
                row.extend("..")
            elif char == "@":
                row.extend("@.")
                items[(len(grid2), len(row) - 2)] = ((len(grid2), len(row) - 1),)
        grid2.append(row)

    robot = find_robot(grid2)
    for command in command_line:
        robot = apply_command2(command, grid2, robot, items)

    return count_score(grid2)


print(f"Part Two: {part_two()}")
