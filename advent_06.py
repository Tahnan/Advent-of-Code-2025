import itertools
from functools import reduce
from pathlib import Path

import aoc_util

TEST_CASE = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
""".strip()


def mul(a, b):
    return a * b


def add(a, b):
    return a + b


def parse_data(data):
    # Too complex, let the parts deal with it
    return data


def part_one(data=TEST_CASE, debug=False):
    lines = data.splitlines()
    space_columns = [i for i, content in enumerate(zip(*lines))
                     if set(content) == {' '}]
    borders = [0] + space_columns + [None]
    lines_in_pieces = [[line[a:b] for a, b in itertools.pairwise(borders)]
                       for line in lines]
    # Are all the columns the same length?  Let's not risk it.
    column_results = []
    for column in zip(*lines_in_pieces):
        column = [x for x in column if x]
        if not column:
            # Did I accidentally pick up trailing spaces or something?
            continue
        op = column.pop().strip()
        if op == '*':
            operation = mul
        elif op == '+':
            operation = add
        else:
            raise RuntimeError('Unknown operation: ' + op)
        column_results.append(reduce(operation, [int(x) for x in column]))
    return sum(column_results)


def part_two(data=TEST_CASE, debug=False):
    lines = data.splitlines()
    space_columns = [i for i, content in enumerate(zip(*lines))
                     if set(content) == {' '}]
    borders = [0] + space_columns + [None]
    lines_in_pieces = [[line[a:b] for a, b in itertools.pairwise(borders)]
                       for line in lines]
    # Are all the columns the same length?  Let's not risk it.
    column_results = []
    for column in zip(*lines_in_pieces):
        column = [x for x in column if x]
        if not column:
            # Did I accidentally pick up trailing spaces or something?
            continue
        op = column.pop().strip()
        if op == '*':
            operation = mul
        elif op == '+':
            operation = add
        else:
            raise RuntimeError('Unknown operation: ' + op)
        actual_column = [''.join(x) for x in zip(*column)
                         if ''.join(x).strip()]
        column_results.append(reduce(operation, [int(x) for x in actual_column]))
    return sum(column_results)


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
