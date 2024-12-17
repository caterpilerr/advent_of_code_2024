input_file = "input.txt"
with open(input_file, "r") as f:
    lines = f.readlines()

data = list(map(int, lines[0].strip().split()))


def func(val: int, steps: int, cache):
    if (val, steps) in cache:
        return cache[(val, steps)]

    if steps == 0:
        return 1

    if val == 0:
        cache[(val, steps)] = func(1, steps - 1, cache)
        return cache[(val, steps)]
    elif len(str(val)) >= 2 and len(str(val)) % 2 == 0:
        mid = len(str(val)) // 2
        left = int(str(val)[:mid])
        right = int(str(val)[mid:])

        cache[(val, steps)] = func(left, steps - 1, cache) + func(
            right, steps - 1, cache
        )
    else:
        cache[(val, steps)] = func(val * 2024, steps - 1, cache)

    return cache[(val, steps)]


global_cache = dict()


def part_one():
    result = 0
    for item in data:
        result += func(item, 25, global_cache)

    return result


print(f"Part One: {part_one()}")


def part_two():
    result = 0
    for item in data:
        result += func(item, 75, global_cache)

    return result


print(f"Part Two: {part_two()}")
