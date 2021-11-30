from typing import Sequence

import input
from re import *


def run(r: Sequence[str]):
    n = [int(k) for k in r]

    li = {v: k for k, v in enumerate(n[:-1])}

    last = n[-1]
    for i in range(len(n), 30000000):
        if last in li:
            newlast = i - li[last] - 1
        else:
            newlast = 0
        li[last] = i - 1
        last = newlast
        if i == 2019:
            print(last)
    print(last)


if __name__ == '__main__':
    day, year = 15, 2020
    input.wait_for_input(day, year)

    split_seq = ','

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
