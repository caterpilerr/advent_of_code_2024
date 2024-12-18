from collections import deque

input_file = "input.txt"
with open(input_file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

height = len(lines)
width = len(lines[0])


DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
LEFT_TURNS = {(0, 1): (1, 0), (0, -1): (-1, 0), (1, 0): (0, -1), (-1, 0): (0, 1)}
RIGHT_TURNS = {(0, 1): (-1, 0), (0, -1): (1, 0), (1, 0): (0, 1), (-1, 0): (0, -1)}


def count_sides(perimeter_cells):
    sides = 0
    for cell, vectors in list(perimeter_cells.items()):
        for vec in vectors:
            sides += 1
            for get_next in (LEFT_TURNS, RIGHT_TURNS):
                next_cell = cell
                next_vec = vec
                while True:
                    dx, dy = get_next[next_vec]
                    next_cell = (next_cell[0] + dx, next_cell[1] + dy)
                    if (
                        next_cell in perimeter_cells
                        and next_vec in perimeter_cells[next_cell]
                    ):
                        perimeter_cells[next_cell].remove(next_vec)
                    else:
                        break

        vectors.clear()

    return sides


def get_region(start_x, start_y, visited):
    region_symbol = lines[start_x][start_y]
    queue = deque([(start_x, start_y)])
    perimeter_cells = {}
    area = perimeter = 0

    while queue:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        area += 1
        for dx, dy in DIRECTIONS:
            next_x, next_y = x + dx, y + dy
            if (
                next_x < 0
                or next_x >= height
                or next_y < 0
                or next_y >= width
                or lines[next_x][next_y] != region_symbol
            ):
                perimeter_cells.setdefault((x, y), set()).add((dx, dy))
                perimeter += 1
            elif (next_x, next_y) not in visited:
                queue.append((next_x, next_y))

    sides = count_sides(perimeter_cells)
    return area, perimeter, sides


visited = set()
regions = list()
for i in range(height):
    for j in range(width):
        if (i, j) in visited:
            continue
        area, perimeter, sides = get_region(i, j, visited)
        regions.append((lines[i][j], area, perimeter, sides))


def part_one():
    return sum(area * perimeter for _, area, perimeter, _ in regions)


print(f"Part One: {part_one()}")


def part_two():
    return sum(area * sides for _, area, _, sides in regions)


print(f"Part Two: {part_two()}")
