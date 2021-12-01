from typing import Sequence

from helpers import input
from re import *
from itertools import *

memo = {}
def rc(h1, h2):
    if (h1, h2) in memo:
        return memo[(h1, h2)]

    oh1 = h1
    oh2 = h2

    prev_seen = []

    while len(h1) and len(h2):
        if (tuple(h1), tuple(h2)) in prev_seen:
            memo[(oh1, oh2)] = (h1, ())
            return (h1, ())
        prev_seen.append((tuple(h1), tuple(h2)))

        c1 = h1[0]
        c2 = h2[0]

        if c1 < len(h1) and c2 < len(h2):
            w = len(rc(h1[1:c1 + 1], h2[1:c2 + 1])[1]) == 0
        else:
            w = c1 > c2

        if w:
            h1 = h1[1:] + (c1, c2)
            h2 = h2[1:]
        else:
            h1 = h1[1:]
            h2 = h2[1:] + (c2, c1)

    memo[(oh1, oh2)] = (h1, h2)
    return (h1, h2)


def run(r: Sequence[str]):
    hands = [[int(k) for k in r[0].splitlines()[1:]], [int(k) for k in r[1].splitlines()[1:]]]

    # while len(hands[0]) and len(hands[1]):
    #     c0 = hands[0][0]
    #     c1 = hands[1][0]
    #
    #     hands[0] = hands[0][1:]
    #     hands[1] = hands[1][1:]
    #
    #     if c0 > c1:
    #         hands[0].extend([max(c0, c1), min(c0, c1)])
    #     else:
    #         hands[1].extend([max(c0, c1), min(c0, c1)])
    # # print(hands[0] + hands[1])
    # print(sum([i * k + k for i, k in enumerate((hands[0] + hands[1])[::-1])]))

    hands = rc(tuple(int(k) for k in r[0].splitlines()[1:]), tuple(int(k) for k in r[1].splitlines()[1:]))
    print(sum([i * k + k for i, k in enumerate((hands[0] + hands[1])[::-1])]))


if __name__ == '__main__':
    day, year = 22, 2020
    input.wait_for_input(day, year)

    split_seq = '\n\n'

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
