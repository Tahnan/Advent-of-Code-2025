from pathlib import Path

import aoc_util

TEST_CASE = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
""".strip()


def parse_data(data):
    # pre-defined in case it's needed
    return [(-1 if dat[0] == 'L' else 1, int(dat[1:])) for dat in data.split()]


def part_one(data=TEST_CASE, debug=False):
    data = parse_data(data)
    setting = 50
    zeroes = 0
    for direction, num in data:
        setting = (setting + num * direction) % 100
        if setting == 0:
            zeroes += 1
    return zeroes


def part_two(data=TEST_CASE, debug=False):
    data = parse_data(data)
    setting = 50
    zeroes = 0
    for direction, abs_distance in data:
        full_rotations, remainder = divmod(abs_distance, 100)
        zeroes += full_rotations
        distance = direction * remainder
        if setting != 0 and not (0 < setting + distance < 100):
            zeroes += 1
        setting = (setting + distance) % 100
        if debug:
            print(direction, abs_distance, setting, zeroes)
    return zeroes


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
