from typing import Sequence

from helpers import input
from util import adj


def run(r: Sequence[str]):
    for dim in (3, 4):
        active = set()
        for y, row in enumerate(r):
            for x, cell in enumerate(row):
                if cell == '#':
                    active.add((x, y) + (0,) * (dim - 2))

        for _ in range(6):
            checked = active.copy()
            activate = set()
            deactivate = set()
            for cell in active:
                adj_cells = adj(cell)
                num_adj = len(active.intersection(adj_cells))
                if num_adj != 2 and num_adj != 3:
                    deactivate.add(cell)
                for adj_cell in adj_cells:
                    if adj_cell in checked:
                        continue
                    adj_cells_2 = adj(adj_cell)
                    num_adj = len(active.intersection(adj_cells_2))
                    if num_adj == 3:
                        activate.add(adj_cell)
            active.difference_update(deactivate)
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
