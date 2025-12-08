import itertools
from pathlib import Path

import aoc_util


TEST_CASE = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""".strip()


def distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** .5


class ShortestDistanceList:
    def __init__(self, size):
        self._size = size
        self._distances = {}
        self._max_distance = 0

    def get_list(self):
        return self._distances.values()

    def add_pair(self, one, two):
        dist = distance(one, two)
        if dist in self._distances:
            # Hoping that the idea is that all distances are unique...
            raise ValueError('Existing distance found!')
        if len(self._distances) < self._size:
            self._max_distance = max(self._max_distance, dist)
            self._distances[dist] = (one, two)
            return
        if dist > self._max_distance:
            return
        self._max_distance = max(self._max_distance, dist)
        self._distances[dist] = (one, two)
        del self._distances[max(self._distances)]


class CircuitMaintainer:
    def __init__(self, boxes_to_anticipate=None):
        self._box_to_circuit = {}
        self._circuit_to_boxes = {}
        self._current_circuit = 1
        self.boxes_to_anticipate = boxes_to_anticipate

    def add_pair(self, one, two):
        current_one = self._box_to_circuit.get(one)
        current_two = self._box_to_circuit.get(two)

        if not current_one and not current_two:
            self._box_to_circuit[one] = self._current_circuit
            self._box_to_circuit[two] = self._current_circuit
            self._circuit_to_boxes[self._current_circuit] = [one, two]
            self._current_circuit += 1
            return

        if current_one == current_two:
            return

        if not current_one:
            self._box_to_circuit[one] = current_two
            self._circuit_to_boxes[current_two].append(one)

        elif not current_two:
            self._box_to_circuit[two] = current_one
            self._circuit_to_boxes[current_one].append(two)

        else:
            boxes_in_two = self._circuit_to_boxes.pop(current_two)
            for box in boxes_in_two:
                self._box_to_circuit[box] = current_one
            self._circuit_to_boxes[current_one] += boxes_in_two

    def get_three_largest(self):
        sizes = [len(circuit) for circuit in self._circuit_to_boxes.values()]
        sizes.sort(reverse=True)
        return sizes[:3]

    def report(self):
        print('Report:')
        for number, boxes in self._circuit_to_boxes.items():
            print(f'  {number:>3}: {len(boxes)}')


def parse_data(data):
    # pre-defined in case it's needed
    return [tuple([int(x) for x in line.split(',')]) for line in data.splitlines()]


def part_one(data=TEST_CASE, debug=False):
    boxes = parse_data(data)
    connections_to_make = 10 if data == TEST_CASE else 1000

    distance_list = ShortestDistanceList(connections_to_make)
    for one, two in itertools.combinations(boxes, 2):
        distance_list.add_pair(one, two)

    circuits = CircuitMaintainer()
    for one, two in distance_list.get_list():
        circuits.add_pair(one, two)
    # if debug:
    #     circuits.report()
    biggest, bigger, big = circuits.get_three_largest()
    return biggest * bigger * big


def part_two(data=TEST_CASE, debug=False):
    boxes = parse_data(data)
    very_naive_list = list(itertools.combinations(boxes, 2))
    very_naive_list.sort(key=lambda x: distance(*x))



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
        (part_two, {}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
