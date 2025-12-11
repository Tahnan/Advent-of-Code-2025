import itertools
from collections import Counter
from math import inf
from pathlib import Path

import aoc_util

TEST_CASE = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""".strip()


def parse_data(data):
    # pre-defined in case it's needed
    machines = []
    for line in data.splitlines():
        indicator, *schematics, joltage = line.split()
        target = {i for i, light in enumerate(indicator[1:-1]) if light == '#'}
        schematics = [[int(x) for x in y[1:-1].split(',')] for y in schematics]
        joltage = [int(x) for x in joltage[1:-1].split(',')]
        machines.append((target, schematics, joltage))
    return machines


def part_one(data=TEST_CASE, debug=False):
    data = parse_data(data)
    button_presses = 0
    for target, buttons, _ in data:
        found = False
        for i in range(1, len(buttons) + 1):
            for pressed in itertools.combinations(buttons, i):
                state = Counter()
                for button in pressed:
                    state.update(button)
                on = {btn for btn, presses in state.items() if presses % 2}
                if on == target:
                    button_presses += i
                    found = True
                    break
            if found:
                break
        else:
            raise ValueError(f'Solution not found: {target}, {buttons}')
    return button_presses


# (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
#
# 1 0 1 1 1
# 0 0 1 1 0
# 1 0 0 0 1
# 1 1 1 0 0
# 1 1 1 1 0
# ---------
# 7 5 C 7 2


def find_minimal_presses(buttons, target, depth=0):
    if sum(target) == 0:
        return 0
    if not buttons:
        return inf
    # do we have only one button for any of them?  That makes it easy.
    for i in range(len(target)):
        btn = [b for b in buttons if i in b]
        if len(btn) == 1:
            remainder = [b for b in buttons if i not in b]
            retarget = list(target)
            for tgt in btn[0]:
                retarget[tgt] -= target[i]
            # print(f'{depth:>{depth}}> Button: {btn[0]} * {target[i]},'
            #       f' Remainder: {remainder}, Target: {retarget}')
            return target[i] + find_minimal_presses(remainder, retarget, depth+1)
    # Otherwise, pick the smallest target
    min_index = min(range(len(target)), key=lambda x: target[x] or inf)
    min_target = target[min_index]
    btn = [b for b in buttons if min_index in b]
    remainder = [b for b in buttons if min_index not in b]
    best = inf
    for combo in itertools.combinations_with_replacement(btn, min_target):
        retarget = list(target)
        for button in combo:
            for i in button:
                retarget[i] -= 1
        if any(t < 0 for t in retarget):
            continue
        # print(f'{depth:>{depth}}> Combo: {combo}, Remainder: {remainder},'
        #       f' Target: {retarget}')
        best = min(best, min_target + find_minimal_presses(remainder, retarget, depth+1))
    return best


# 12:22 - setting aside
# why does this feel like it's just matrix math?
def part_two(data=TEST_CASE, debug=False):
    data = parse_data(data)
    button_presses = 0
    for _, buttons, target in data:
        if debug:
            print(buttons, target)
        presses = find_minimal_presses(buttons, target)
        button_presses += presses
        if debug:
            print('---', presses, '---')
    return button_presses


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
        (part_two, {'data': DATA, 'debug': True}),
    ):
        start_time = time.monotonic()
        result = fn(**kwargs)
        time_taken = f"{time.monotonic() - start_time :.3}:"
        print(f'{time_taken:<6} {result}')
