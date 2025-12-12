from collections import Counter
from pathlib import Path

import aoc_util

TEST_CASE = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
""".strip()

TEST_CASE_TWO = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
""".strip()


def parse_data(data):
    network_map = {}
    for line in data.strip().splitlines():
        origin, dest = line.split(': ')
        network_map[origin] = set(dest.split())
    return network_map


def part_one(data=TEST_CASE, debug=False):
    network_map = parse_data(data)
    current_paths = {('you',)}
    paths_found = 0
    while current_paths:
        new_paths = set()
        for path in current_paths:
            for dest in network_map[path[-1]]:
                if dest == 'out':
                    paths_found += 1
                else:
                    new_paths.add(path + (dest,))
        current_paths = new_paths
    return paths_found


DAC = 1
FFT = 2


# Rethink: if there are no loops (and there really can't be, because otherwise
# infinite paths, right?), then both DAC and FFT are chokepoints: everything
# has to run from SVR to DAC, from DAC to FFT, and from FFT to OUT.  (Or, sadly,
# switch DAC and FFT.)  We don't need to go all the way from SVR to OUT.
def order_dac_and_fft(network):
    seen = {'out'}
    new = {'dac'}
    while new:
        # Just trace the places we've been; we don't need paths right now
        seen.update(new)
        new.discard('out')
        new = set.union(*[network[loc] for loc in new]) - seen
    if 'fft' in seen:
        # We started at 'dac'.  If 'fft' was seen, it means we'll go to dac
        # first, fft second.
        return 'dac', 'fft'
    # Otherwise, we'll have to go to 'fft' before 'dac'.
    return 'fft', 'dac'


def part_two(data=TEST_CASE_TWO, debug=False):
    network = parse_data(data)
    # First: is it DAC --> FFT or FFT --> DAC?
    print('Parsing network...')
    one, two = order_dac_and_fft(network)
    print('...parsed.  Finding paths...')
    total_paths = 1
    # If you hit one of these (and it's not your endpoint in this part of the
    # loop), you've gone off course.  After running from [two] to "out", we'll
    # add any nodes we saw on that route as well; and so forth.
    useless = {'dac', 'fft', 'out'}
    for pair in ((two, 'out'), (one, two), ('svr', one)):
        print(f'...between {pair}...')
        start, end = pair
        unwanted = useless - {start, end}
        paths = {start: 1}
        found = 0
        seen = set()
        while paths:
            new_paths = Counter()
            for loc, count in paths.items():
                for dest in network[loc]:
                    if dest in unwanted:
                        continue
                    elif dest == end:
                        found += count
                    else:
                        new_paths[dest] += count
                        seen.add(dest)
            paths = new_paths
            print(' >', len(paths), sum(paths.values()), found)
        total_paths *= found
        useless.update(seen)
    return total_paths


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print('Starting:', time.ctime())
    for fn, kwargs in (
        (part_one, {}),
        (part_one, {'data': DATA}),
        (part_two, {}),
        (part_two, {'debug': True, 'data': DATA}),
    ):
        start_time = time.monotonic()
        result = fn(**kwargs)
        time_taken = f"{time.monotonic() - start_time :.3}:"
        print(f'{time_taken:<6} {result}')
