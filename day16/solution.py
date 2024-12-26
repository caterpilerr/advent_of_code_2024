from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from collections import deque
from itertools import combinations


input_file = "input.txt"
with open(input_file, "r") as f:
    lines = [line.strip() for line in f.readlines()]


def find_starting_index(lines):
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "S":
                return (i, j)

    raise ValueError("No starting index found")


DIRECTIONS = {(0, 1), (0, -1), (1, 0), (-1, 0)}


def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1]


def reverse_direction(dir):
    return (-dir[0], -dir[1])


def build_graph(lines):
    nodes = set()
    queue = deque()
    vertices = set()
    queue.append((find_starting_index(lines), (0, 1)))
    while queue:
        node, start_dir = queue.popleft()
        current_cell = node
        current_dir = start_dir
        current_length = 1

        now_way = False
        while True:
            all_dirs = set()
            for dir in DIRECTIONS:
                next_cell = (current_cell[0] + dir[0], current_cell[1] + dir[1])
                if lines[next_cell[0]][next_cell[1]] != "#":
                    all_dirs.add(dir)

            next_dirs = all_dirs.difference({reverse_direction(current_dir)})
            if (
                len(next_dirs) == 1
                and lines[current_cell[0]][current_cell[1]] != "E"
                and lines[current_cell[0]][current_cell[1]] != "S"
            ):
                new_dir = next_dirs.pop()
                if current_dir == new_dir:
                    current_length += 1
                else:
                    current_length += 1001
                current_cell = (
                    current_cell[0] + new_dir[0],
                    current_cell[1] + new_dir[1],
                )
                current_dir = new_dir
            elif (
                len(next_dirs) > 1
                or lines[current_cell[0]][current_cell[1]] == "E"
                or lines[current_cell[0]][current_cell[1]] == "S"
            ):
                if node != current_cell:
                    start_node = (node[0] - start_dir[0], node[1] - start_dir[1])
                    vertices.add(
                        (
                            start_node,
                            start_dir,
                            current_cell,
                            current_dir,
                            current_length,
                        )
                    )
                    vertices.add(
                        (
                            current_cell,
                            reverse_direction(current_dir),
                            start_node,
                            reverse_direction(start_dir),
                            current_length,
                        )
                    )
                break
            else:
                now_way = True
                break

        if now_way:
            continue

        if (current_cell, current_dir) in nodes:
            continue

        nodes.add((current_cell, current_dir))

        for dir1, dir2 in combinations(DIRECTIONS, 2):
            if dir1 == dir2:
                continue
            dp = dot_product(dir1, dir2)
            if dp == 0:
                vertices.add((current_cell, dir1, current_cell, dir2, 1000))
                vertices.add((current_cell, dir2, current_cell, dir1, 1000))
            else:
                vertices.add((current_cell, dir1, current_cell, dir2, 2000))
                vertices.add((current_cell, dir2, current_cell, dir1, 2000))

        for dir in DIRECTIONS:
            nodes.add((current_cell, dir))

        for dir in all_dirs:
            if dir != reverse_direction(current_dir):
                next_cell = (current_cell[0] + dir[0], current_cell[1] + dir[1])
                queue.append((next_cell, dir))

    return list(nodes), vertices


def build_adjacency_matrix(nodes, vertices):
    n = len(nodes)
    adj = [[0] * n for _ in range(n)]

    for v in vertices:
        start_node, start_dir, end_node, end_dir, length = v
        start_index = nodes.index((start_node, start_dir))
        end_index = nodes.index((end_node, end_dir))
        adj[start_index][end_index] = length

    return adj


def count_unique_cells(graph, path):
    unique_cells = set()
    for i, node in enumerate(path[:-1]):
        start_cell, start_dir = graph[node]
        dest_cell, _ = graph[path[i + 1]]
        current_cell = start_cell
        current_dir = start_dir
        while True:
            unique_cells.add(current_cell)
            if current_cell == dest_cell:
                break

            next_cell = (
                current_cell[0] + current_dir[0],
                current_cell[1] + current_dir[1],
            )
            if lines[next_cell[0]][next_cell[1]] == "#":
                for dir in DIRECTIONS:
                    if dir == reverse_direction(current_dir):
                        continue
                    if lines[current_cell[0] + dir[0]][current_cell[1] + dir[1]] == "#":
                        continue

                    current_dir = dir
                    break

            current_cell = (
                current_cell[0] + current_dir[0],
                current_cell[1] + current_dir[1],
            )

    return unique_cells


def build_predecessors(graph, distances):
    n_nodes = graph.shape[0]
    all_predecessors = [[] for _ in range(n_nodes)]
    for u, v in zip(*graph.nonzero()):
        if distances[v] == distances[u] + graph[u, v]:
            all_predecessors[v].append(u)

    return all_predecessors


def find_all_paths(predecessors, start, end):
    paths = []

    def backtrack(current_path, node):
        if node == start:
            paths.append(current_path[::-1])
            return
        for pred in predecessors[node]:
            backtrack(current_path + [pred], pred)

    backtrack([end], end)
    return paths


n, v = build_graph(lines)
adj = build_adjacency_matrix(n, v)
end_indexes = []
for node in n:
    if lines[node[0][0]][node[0][1]] == "S" and node[1] == (0, 1):
        start_index = n.index(node)
    if lines[node[0][0]][node[0][1]] == "E":
        end_indexes.append(n.index(node))

graph = csr_matrix(adj)
dist_matrix = dijkstra(csgraph=graph, directed=True, indices=start_index)

end_distances = []
for end_index in end_indexes:
    end_distances.append((end_index, dist_matrix[end_index]))

min_distance = min(end_distances, key=lambda x: x[1])[1]
min_indexies = [
    end_index for end_index, distance in end_distances if distance == min_distance
]

start_node = start_index
all_predecessors = build_predecessors(graph, dist_matrix)
all_paths = []
for min_index in min_indexies:
    all_paths.extend(find_all_paths(all_predecessors, start_node, min_index))

unique_cells = set()
for path in all_paths:
    unique_cells.update(count_unique_cells(n, path))


def part_one():
    return int(min_distance)


print(f"Part One: {part_one()}")


def part_two():
    return len(unique_cells)


print(f"Part Two: {part_two()}")
