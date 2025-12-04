from pathlib import Path

import aoc_util

TEST_CASE = """
""".strip()


def parse_data(data):
    # pre-defined in case it's needed
    return data


def part_one(data=TEST_CASE, debug=False):
    data = parse_data(data)


def part_two(data=TEST_CASE, debug=False):
    data = parse_data(data)


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
