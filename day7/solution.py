import regex as re
from itertools import product

input_file = 'input.txt'
pattern = re.compile(r'\d+')
data = []
with open(input_file, 'r') as f:
    for line in f.readlines():
        line_item = list(map(int, pattern.findall(line)))
        data.append(line_item)

SET1 = ['+', '*']
SET2 = ['+', '*', '||']


def evaluate(operands, operators):
    '''Evaluate the expression based on the operands and operators'''
    result = operands[0]
    for i, op in enumerate(operators):
        if op == '+':
            result += operands[i + 1]
        elif op == '*':
            result *= operands[i + 1]
        elif op == '||':
            result = int(str(result) + str(operands[i + 1]))
    return result

def solve(data, operator_set):
    '''Solve the puzzle based on the operator set'''
    result = 0
    operator_cache = {}
    
    for line in data:
        expected, operands = line[0], line[1:]
        n = len(operands) - 1
        
        # Generate operator combinations (cached)
        if n not in operator_cache:
            operator_cache[n] = list(product(operator_set, repeat=n))
        
        for operators in operator_cache[n]:
            if evaluate(operands, operators) == expected:
                result += expected
                break

    return result        


def evaluate(operands, operators):
    result = operands[0]
    for i in range(len(operators)):
        if operators[i] == '+':
            result += operands[i + 1]
        elif operators[i] == '*':
            result *= operands[i + 1]
        elif operators[i] == '||':
            result = int(str(result) + str(operands[i + 1]))

    return result
    
def part_one():
    return solve(data, SET1)

print(f'Part One: {part_one()}')

def part_two():
    return solve(data, SET2)

print(f'Part Two: {part_two()}')
