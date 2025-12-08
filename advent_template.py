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

    print('Starting:', time.ctime())
    for fn, kwargs in (
        (part_one, {'debug': True}),
        (part_one, {'data': DATA}),
        (part_two, {}),
        (part_two, {'data': DATA}),
    ):
        start_time = time.monotonic()
        result = fn(**kwargs)
        time_taken = f"{time.monotonic() - start_time :.3}:"
        print(f'{time_taken:<6} {result}')
