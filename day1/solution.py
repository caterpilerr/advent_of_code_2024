import collections

input_file = 'input.txt'
with open(input_file, 'r') as f:
    lines = f.readlines()

left = []
right = []
for line in lines:
    a, b = line.strip().split()
    left.append(int(a))
    right.append(int(b))

def part_one():
    left.sort()
    right.sort()

    result = sum(abs(a - b) for a, b in zip(left, right))
    
    return result

print(f'Part One: {part_one()}')

def part_two():
    result = 0
    right_counts = collections.Counter(right)
    for i in left:
        result += i * right_counts[i]

    return result

print(f'Part Two: {part_two()}')
