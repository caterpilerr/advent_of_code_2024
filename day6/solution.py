input_file = 'input.txt'
with open(input_file, 'r') as f:
    grid = [list(line.strip()) for line in f]

map_height = len(grid)
map_width = len(grid[0])

player_pos_start = None
player_dir_start = (-1, 0)

# Locate player start position
for x, row in enumerate(grid):
    for y, cell in enumerate(row):
        if cell == '^':
            player_pos_start = (x, y)
            break
    if player_pos_start:
        break

def turn_left(direction):
    return direction[1], -direction[0]

def part_one():
    '''Count the number of visited cells'''
    x, y = player_pos_start
    player_dir = player_dir_start
    visited = set()

    while True:
        visited.add((x, y))
        next_x, next_y = x + player_dir[0], y + player_dir[1]

        if not (0 <= next_x < map_height and 0 <= next_y < map_width):
            break
        if grid[next_x][next_y] == '#':
            player_dir = turn_left(player_dir)
        else:
            x, y = next_x, next_y

    return len(visited)

print(f'Part One: {part_one()}')

def check_cycle(player_start, player_dir):
    '''Check if the player gets into a cycle starting from a position'''
    x, y = player_start
    visited = set()

    while True:
        state = (x, y, player_dir)
        if state in visited:
            return True
        visited.add(state)

        next_x, next_y = x + player_dir[0], y + player_dir[1]
        if not (0 <= next_x < map_height and 0 <= next_y < map_width):
            return False

        if grid[next_x][next_y] == '#':
            player_dir = turn_left(player_dir)
        else:
            x, y = next_x, next_y

def part_two():
    '''Count the number of positions that would lead to a cycle if converted to obstacles'''
    result = 0

    for x in range(map_height):
        for y in range(map_width):
            if grid[x][y] == '.':
                grid[x][y] = '#'
                if check_cycle(player_pos_start, player_dir_start):
                    result += 1
                grid[x][y] = '.'

    return result

print(f'Part Two: {part_two()}')