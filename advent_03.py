from pathlib import Path

import aoc_util

TEST_CASE = """
987654321111111
811111111111119
234234234234278
818181911112111
""".strip()


def parse_data(data):
    # pre-defined in case it's needed
    pass


def part_one(data=TEST_CASE, debug=False):
    jolts = []
    for line in data.splitlines():
        for i in range(9, 0, -1):
            i = str(i)
            if i in line[:-1]:
                second = max(line[line.index(i) + 1:])
                jolts.append(int(i + second))
                break
    return sum(jolts)


def part_two(data=TEST_CASE, debug=False):
    jolts = []
    for line in data.splitlines():
        running_total = ''
        for digit_number in range(-11, 1):
            if digit_number == 0:
                digit_number = None
            for i in range(9, 0, -1):
                i = str(i)
                if i in line[:digit_number]:
                    running_total += i
                    line = line[line.index(i) + 1:]
                    break
        jolts.append(int(running_total))
    if debug:
        print(*jolts, sep='\n')
    return sum(jolts)


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
