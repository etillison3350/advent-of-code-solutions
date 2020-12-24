from typing import Sequence

import input
from re import *


dir_map = {'e': (1, 0), 'w': (-1, 0), 'ne': (1, -1), 'nw': (0, -1), 'se': (0, 1), 'sw': (-1, 1)}
dir_vectors = tuple(dir_map.values())


def adjacent_hexes(x, y):
    return [(x + dx, y + dy) for dx, dy in dir_vectors]


def num_black_adjacent(x, y, black_tiles):
    n = 0
    for x, y in adjacent_hexes(x, y):
        if (x, y) in black_tiles:
            n += 1
    return n


def run(r: Sequence[str]):
    black_tiles = set()

    for instr in r:
        x, y = 0, 0
        directions = findall('[ns]?[ew]', instr)
        for d in directions:
            dx, dy = dir_map[d]
            x += dx
            y += dy
        if (x, y) in black_tiles:
            black_tiles.remove((x, y))
        else:
            black_tiles.add((x, y))
    print(len(black_tiles))

    for _ in range(100):
        new_black_tiles = set()
        for bx, by in black_tiles:
            num_adj = num_black_adjacent(bx, by, black_tiles)
            if num_adj == 1 or num_adj == 2:
                new_black_tiles.add((bx, by))
            for ax, ay in adjacent_hexes(bx, by):
                if (ax, ay) not in black_tiles:
                    num_adj = num_black_adjacent(ax, ay, black_tiles)
                    if num_adj == 2:
                        new_black_tiles.add((ax, ay))
        black_tiles = new_black_tiles
    print(len(black_tiles))


if __name__ == '__main__':
    day, year = 24, 2020
    input.wait_for_input(day, year)

    split_seq = '\n'

    inp = input.input_text(day, year)
    input_lines = inp.split(split_seq)

    print('True output:')
    run(input_lines)
    print()

    print('Possible test cases:')
    test_cases = input.find_test_cases(day, year, cached=True)
    for index, tc in enumerate(test_cases):
        tc_list = tc.split(split_seq)
        tc_str = str(tc_list)
        print('Test case {}: {}{}'.format(index, tc_str[:80], '...' if len(tc_str) > 80 else ''))
        try:
            run(tc_list)
        except Exception as ex:
            print('{}: {}'.format(type(ex).__name__, ex))
        finally:
            print('Done with test case {}'.format(index))
