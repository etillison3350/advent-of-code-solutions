from typing import Sequence

import input
from re import *


def run(r: Sequence[str]):
    print(r)
    print(len(r))


if __name__ == '__main__':
    day, year = 13, 2020
    input.wait_for_input(day, year)

    split_seq = '\n'

    inp = input.input_text(day, year)
    input_lines = inp.split(split_seq)

    print('True output:')
    run(input_lines)
    print()

    print('Possible test cases:')
    test_cases = input.find_test_cases(day, year, cached=False)
    for index, tc in enumerate(test_cases):
        tc_list = tc.split(split_seq)
        print('Test case {}: {}'.format(index, str(tc_list)[:80]))
        try:
            run(tc_list)
        except Exception as ex:
            print('{}: {}'.format(type(ex).__name__, ex))
        finally:
            print('Done with test case {}'.format(index))
