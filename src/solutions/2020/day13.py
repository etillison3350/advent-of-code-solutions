from typing import Sequence

from helpers import input
import math


def run(r: Sequence[str]):
    now = int(r[0])
    buses = [int(k) for k in r[1].split(',') if k != 'x']
    next_time = [(math.ceil(now / j) * j, j) for j in buses]

    bus = min(next_time)
    print(bus)
    print((bus[0] - now) * bus[1])

    buses = [(int(k), i) for i, k in enumerate(r[1].split(',')) if k != 'x']
    product = 1
    for a, _ in buses:
        product *= a

    ans = 0
    for n, i in buses:
        q = product // n
        for v in range(n):
            if q * v % n == 1:
                ans -= i * q * v
                break
    print(ans % product)


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
    test_cases = input.find_test_cases(day, year, cached=True)
    for index, tc in enumerate(test_cases):
        tc_list = tc.split(split_seq)
        print('Test case {}: {}'.format(index, str(tc_list)[:80]))
        try:
            run(tc_list)
        except Exception as ex:
            print('{}: {}'.format(type(ex).__name__, ex))
        finally:
            print('Done with test case {}'.format(index))
