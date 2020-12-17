from typing import Sequence

from itertools import product

import input
from re import *


def adj(co):
    d = len(co)
    return {tuple(a[i] + co[i] for i in range(d)) for a in product((-1, 0, 1), repeat=d) if a != ((0,) * d)}


def run(r: Sequence[str]):
    for dim in (3, 4):
        active = set()
        for y, row in enumerate(r):
            for x, cell in enumerate(row):
                if cell == '#':
                    active.add((x, y) + (0,) * (dim - 2))

        for iter in range(6):
            checked = active.copy()
            activate = set()
            deac = set()
            for cell in active:
                a = adj(cell)
                na = len(active.intersection(a))
                if na != 2 and na != 3:
                    deac.add(cell)
                for ad in a:
                    if ad in checked:
                        continue
                    a2 = adj(ad)
                    na2 = len(active.intersection(a2))
                    if na2 == 3:
                        activate.add(ad)
            active.difference_update(deac)
            active.update(activate)
        print(len(active))


if __name__ == '__main__':
    day, year = 17, 2020
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
