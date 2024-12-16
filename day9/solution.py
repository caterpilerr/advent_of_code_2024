from collections import OrderedDict

input_file = "input.txt"
with open(input_file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

memory = []
data_line = lines[0] + "0"
k = 0
for i in range(0, len(data_line), 2):
    memory.append([int(data_line[i]), int(data_line[i + 1]), i // 2, k])
    k += int(data_line[i]) + int(data_line[i + 1])

mem_array = []
for m in memory:
    for i in range(m[0]):
        mem_array.append(m[2])
    for i in range(m[1]):
        mem_array.append(-1)


def compact(data):
    left, right = 0, len(data) - 1
    while left < right:
        if data[left] == -1 and data[right] != -1:
            data[left], data[right] = data[right], -1
            left += 1
            right -= 1
        elif data[left] != -1:
            left += 1
        else:
            right -= 1
    return data


def part_one():
    compacted = compact(mem_array.copy())
    return sum(value * idx for idx, value in enumerate(compacted) if value != -1)


print(f"Part One: {part_one()}")


def part_two():
    files = OrderedDict()
    empty_blocks = []
    for block_size, empty_size, block_id, start in memory:
        files[block_id] = (start, block_size)
        empty_blocks.append([start + block_size, empty_size])

    for fid, (file_start, file_length) in reversed(files.items()):
        i = 0
        while i < len(empty_blocks):
            empty_start, empty_length = empty_blocks[i]
            if empty_start > file_start:
                break
            if empty_length >= file_length:
                files[fid] = (empty_start, file_length)
                if empty_length > file_length:
                    empty_blocks[i][0] += file_length
                    empty_blocks[i][1] -= file_length
                else:
                    empty_blocks.pop(i)
                break
            i += 1

    result = 0
    for fid, (start, length) in files.items():
        result += sum(start + i for i in range(length)) * fid
    return result


print(f"Part Two: {part_two()}")
