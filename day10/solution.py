from collections import deque

input_file = "input.txt"
with open(input_file, "r") as f:
    lines = [list(map(int, line.strip())) for line in f.readlines()]


def mark_trail(heads, start_x, start_y, unique=True):
    queue = deque([(start_x, start_y)])
    visited = set((start_x, start_y))
    while queue:
        x, y = queue.popleft()
        if unique and (x, y) in visited:
            continue

        visited.add((x, y))

        if lines[x][y] == 0:
            if (x, y) in heads:
                heads[(x, y)] += 1
            else:
                heads[(x, y)] = 1

        dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in dir:
            new_x, new_y = x + dx, y + dy
            if new_x < 0 or new_x >= len(lines) or new_y < 0 or new_y >= len(lines[0]):
                continue
            if lines[x][y] - lines[new_x][new_y] == 1:
                queue.append((new_x, new_y))


def part_one():
    heads = {}
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == 9:
                mark_trail(heads, i, j)

    result = result = sum(item for item in heads.values())

    return result


print(f"Part One: {part_one()}")


def part_two():
    heads = {}
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == 9:
                mark_trail(heads, i, j, unique=False)

    result = sum(item for item in heads.values())

    return result


print(f"Part Two: {part_two()}")
