input_file = "input.txt"
with open(input_file, "r") as f:
    lines = [line.strip() for line in f.readlines()]


raw_rules = lines[: lines.index("")]
updates = [list(map(int, line.split(","))) for line in lines[lines.index("") + 1 :]]


before_rules = {}
for rule in raw_rules:
    raw_before, raw_after = rule.split("|")
    before = int(raw_before)
    after = int(raw_after)
    if after in before_rules:
        before_rules[after].add(before)
    else:
        before_rules[after] = set()
        before_rules[after].add(before)


def check_update(update: list[int], before_rules: dict[int, set[int]]) -> int:
    """Check if an update is valid based on rules"""
    seen = set()
    for i in range(len(update) - 1, -1, -1):
        if update[i] in before_rules and seen & before_rules[update[i]]:
            return False
        seen.add(update[i])
    return True


def build_order(updates: set[int], before_rules: dict[int, set[int]]) -> list[int]:
    """Reorder updates based on rules"""
    if not updates:
        return []
    current = updates.pop()
    if not updates:
        return [current]
    before = before_rules.get(current, set()).intersection(updates)
    rest = updates.difference(before)
    return (
        build_order(before, before_rules) + [current] + build_order(rest, before_rules)
    )


def part_one() -> int:
    total = 0
    for update in updates:
        if check_update(update, before_rules):
            middle = update[len(update) // 2]
            total += middle
    return total


print(f"Part One: {part_one()}")


def part_two() -> int:
    total = 0
    for update in updates:
        if not check_update(update, before_rules):
            reordered_update = build_order(set(update), before_rules)
            middle = reordered_update[len(reordered_update) // 2]
            total += middle
    return total


print(f"Part Two: {part_two()}")
