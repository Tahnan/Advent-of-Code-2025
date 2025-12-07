from collections import Counter
from pathlib import Path

import aoc_util

TEST_CASE = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
""".strip()


def parse_data(data):
    # pre-defined in case it's needed
    lines = data.splitlines()
    start = None
    splitters = set()
    for row, line in enumerate(lines):
        for col, element in enumerate(line):
            if element == 'S':
                start = (row, col)
            elif element == '^':
                splitters.add((row, col))
    return start, splitters


def part_one(data=TEST_CASE, debug=False):
    (current_row, start_col), splitters = parse_data(data)
    columns = {start_col}
    max_row, max_col = [max(dim) for dim in zip(*splitters)]
    splits = 0
    while current_row <= max_row:
        current_row += 1
        new_columns = set()
        for column in columns:
            if (current_row, column) in splitters:
                splits += 1
                new_columns.update((column - 1, column + 1))
            else:
                new_columns.add(column)
        columns = new_columns
    return splits


def part_two(data=TEST_CASE, debug=False):
    (current_row, start_col), splitters = parse_data(data)
    columns = Counter({start_col: 1})
    max_row, max_col = [max(dim) for dim in zip(*splitters)]
    while current_row <= max_row:
        current_row += 1
        new_columns = Counter()
        for column, count in columns.items():
            if (current_row, column) in splitters:
                new_columns.update({column - 1: count, column + 1: count})
            else:
                new_columns[column] += count
        columns = new_columns
    return sum(columns.values())


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    for fn, kwargs in (
        (part_one, {}),
        (part_one, {'data': DATA}),
        (part_two, {}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
