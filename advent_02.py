from math import log
from pathlib import Path

import aoc_util

TEST_CASE = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
""".strip()


def parse_data(data):
    # pre-defined in case it's needed
    return [[int(n) for n in rng.split('-')] for rng in data.split(',')]


def part_one(data=TEST_CASE, debug=False):
    invalid_ids = []
    for low, high in parse_data(data):
        if debug:
            print(low, high, end='\t')
        low_magnitude = len(str(low))
        if low_magnitude % 2:
            low = 10 ** low_magnitude
            low_magnitude += 1
        high_magnitude = len(str(high))
        if high_magnitude % 2:
            high = (10 ** (high_magnitude - 1)) - 1
            high_magnitude -= 1

        half_low = int(low // (10 ** (low_magnitude / 2)))
        half_high = int(high // (10 ** (high_magnitude / 2)))
        if debug:
            print(low, high, end='\t')
            print(half_low, half_high + 1)
        for n in range(half_low, half_high + 1):
            maybe_bad = int(str(n) * 2)
            if low <= maybe_bad <= high:
                invalid_ids.append(maybe_bad)

    return sum(invalid_ids)


def part_two(data=TEST_CASE, debug=False):
    invalid_ids = set()
    for low, high in parse_data(data):
        if debug:
            print(low, high)
        high_magnitude = len(str(high))

        hm = high_magnitude if high_magnitude % 2 == 0 else high_magnitude + 1
        upper_bound = int(max(high, 10 ** hm) / (10 ** (hm // 2)))
        if debug:
            print('*', hm, high, upper_bound)
        for prefix in range(1, upper_bound):
            repeats = 2
            while True:
                maybe_bad = int(str(prefix) * repeats)
                if maybe_bad > high:
                    break
                if maybe_bad >= low:
                    invalid_ids.add(maybe_bad)
                    if debug:
                        print('   ', 'Found:', maybe_bad)
                repeats += 1

    return sum(invalid_ids)


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    for fn, kwargs in (
        (part_one, {'debug': True}),
        (part_one, {'data': DATA}),
        (part_two, {'debug': True}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
