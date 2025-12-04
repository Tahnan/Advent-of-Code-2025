from pathlib import Path

import aoc_util
from grid_util import Grid

TEST_CASE = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".strip()


def parse_data(data):
    # pre-defined in case it's needed
    return Grid.from_text(data)


def part_one(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    accessible = 0
    for square, content in grid.items():
        if content == '@' and grid.get_neighbors(square, diagonals=True).count('@') < 4:
            accessible += 1
    return accessible


def part_two(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    removable = 0
    currently_removable = 'dummy value'
    while currently_removable:
        currently_removable = {}
        for square, content in grid.items():
            if (content == '@' and
                grid.get_neighbors(square, diagonals=True).count('@') < 4):
                removable += 1
                currently_removable[square] = '.'
        grid.update(currently_removable)
    return removable


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
