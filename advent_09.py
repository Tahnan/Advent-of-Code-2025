import itertools
from pathlib import Path

from PIL import Image, ImageDraw

import aoc_util

TEST_CASE = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
""".strip()


def parse_data(data):
    # pre-defined in case it's needed
    return [tuple(int(x) for x in line.split(',')) for line in data.splitlines()]


def part_one(data=TEST_CASE, debug=False):
    data = parse_data(data)
    max_area = 0
    for (x1, y1), (x2, y2) in itertools.combinations(data, 2):
        new_area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
        max_area = max(max_area, new_area)
    return max_area


# Hey, look, it's borrowed from Day 5!
def condense(ranges):
    ranges.sort()
    condensed = []
    for a, b in ranges:
        if not condensed or a > condensed[-1][1]:
            condensed.append([a, b])
        else:
            condensed[-1][1] = max(condensed[-1][1], b)
    return condensed


class GreenTiles:
    """
    Given coordinate pairs, work out--for each column x, and each row y--what
    ranges contain green tiles.

    Then, given two coordinates of a rectangle, see whether all four of its
    edges are contained within those ranges.  (And then we don't need to check
    the interior, because something something geometry.)
    """
    def __init__(self, coordinate_pairs):
        # We know they alternate, but determining which one is first and then
        # taking alternate pairs is too much work.  Also: horizontal? vertical?
        # it really doesn't matter, it's just a reflection along x=y.
        vertical_lines = {}
        horizontal_lines = {}
        horiz_to_add = {}
        vert_to_add = {}
        looped = coordinate_pairs + [coordinate_pairs[0]]
        for (x1, y1), (x2, y2) in itertools.pairwise(looped):
            if x1 == x2:
                small, large = sorted((y1, y2))
                for y in range(small, large):
                    vertical_lines.setdefault(y, []).append(x1)
                horiz_to_add.setdefault(x1, []).append([small, large])
            elif y1 == y2:
                small, large = sorted((x1, x2))
                # purposefully leave off the top!
                for x in range(small, large):
                    horizontal_lines.setdefault(x, []).append(y1)
                vert_to_add.setdefault(y1, []).append([small, large])
            else:
                raise RuntimeError

        self._vertical = {}
        self._horizontal = {}
        for y, line in vertical_lines.items():
            line.sort()
            ranges = [line[2*i:2*i+2] for i in range(int(len(line) // 2))]
            ranges.extend(vert_to_add.get(y, ()))
            self._vertical[y] = condense(ranges)
        for x, line in horizontal_lines.items():
            line.sort()
            ranges = [line[2*i:2*i+2] for i in range(int(len(line) // 2))]
            ranges.extend(horiz_to_add.get(x, ()))
            self._horizontal[x] = condense(ranges)

    def is_rectangle_green(self, one, two):
        xs, ys = zip(one, two)
        x1, x2 = sorted(xs)
        y1, y2 = sorted(ys)
        if y1 not in self._vertical or y2 not in self._vertical:
            return False
        if x1 not in self._horizontal or x2 not in self._horizontal:
            return False
        if not any(s <= y1 <= y2 <= e for s, e in self._horizontal[x1]):
            return False
        if not any(s <= y1 <= y2 <= e for s, e in self._horizontal[x2]):
            return False
        if not any(s <= x1 <= x2 <= e for s, e in self._vertical[y1]):
            return False
        if not any(s <= x1 <= x2 <= e for s, e in self._vertical[y2]):
            return False
        return True


def part_two(data=TEST_CASE, debug=False):
    data = parse_data(data)
    max_area = 0
    green_checker = GreenTiles(data)
    for (x1, y1), (x2, y2) in itertools.combinations(data, 2):
        new_area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
        if debug:
            print((x1, y1), (x2, y2), new_area)
        if new_area <= max_area:
            continue
        if green_checker.is_rectangle_green((x1, y1), (x2, y2)):
            if debug:
                print('> ...is green!')
            max_area = new_area
    return max_area


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
