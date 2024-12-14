from itertools import combinations

input_file = "input.txt"
with open(input_file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

height = len(lines)
width = len(lines[0])


def parse_antennas(lines):
    '''Parse the antennas from the input file'''
    antennas = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ".":
                antennas.setdefault(char, set()).add((x, y))
    return antennas


antennas = parse_antennas(lines)


def calculate_antinodes(antennas, width, height, extend=False):
    '''Calculate the number of antinodes'''
    antinodes = set()
    for ant_loc in antennas.values():
        for ant1, ant2 in combinations(ant_loc, 2):
            antinodes.add(ant1)
            dx, dy = ant2[0] - ant1[0], ant2[1] - ant1[1]
            for multiplier in [-1, 1]:
                x, y = ant1[0] + multiplier * dx, ant1[1] + multiplier * dy
                while 0 <= x < width and 0 <= y < height:
                    antinodes.add((x, y))
                    if not extend:
                        break
                    x += multiplier * dx
                    y += multiplier * dy
    return len(antinodes)


def part_one():
    return calculate_antinodes(antennas, width, height, extend=False)


print(f"Part One: {part_one()}")


def part_two():
    return calculate_antinodes(antennas, width, height, extend=True)


print(f"Part Two: {part_two()}")
