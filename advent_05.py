from pathlib import Path

import aoc_util

TEST_CASE = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
""".strip()


def parse_data(data):
    # pre-defined in case it's needed
    ranges, stock = data.split('\n\n')
    ranges = [[int(x) for x in y.split('-')] for y in ranges.splitlines()]
    ranges.sort()
    stock = [int(x) for x in stock.splitlines()]
    return ranges, stock


def part_one(data=TEST_CASE, debug=False):
    ranges, stock = parse_data(data)
    fresh = 0
    for item in stock:
        for a, b in ranges:
            if a <= item <= b:
                fresh += 1
                break
            if item < a:
                break
    return fresh


def part_two(data=TEST_CASE, debug=False):
    ranges, _ = parse_data(data)
    condensed = []
    for a, b in ranges:
        if not condensed or a > condensed[-1][1]:
            condensed.append([a, b])
        else:
            condensed[-1][1] = max(condensed[-1][1], b)
    if debug:
        print(condensed)
    return sum(b - a + 1 for a, b in condensed)


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
        (part_two, {'debug': True}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
