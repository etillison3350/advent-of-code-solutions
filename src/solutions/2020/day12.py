from typing import Sequence
import sys

from helpers import input
from re import *

left = {'E': 'N', 'S': 'E', 'W': 'S', 'N': 'W'}
right = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}

mv = {'E': (1, 0), 'N': (0, 1), 'W': (-1, 0), 'S':  (0, -1)}


def run(r: Sequence[str]):
    ch = 'E'
    x = 0
    y = 0
    for dir in r:
        cmd = dir[0]
        dist = int(dir[1:])
        if cmd == 'L':
            for i in range(0, dist, 90):
                ch = left[ch]
        elif cmd == 'R':
            for i in range(0, dist, 90):
                ch = right[ch]
        else:
            if cmd == 'F':
                cmd = ch
            dx, dy = mv[cmd]
            x += dx * dist
            y += dy * dist
    print(abs(x) + abs(y))

    wp = [10, 1]
    x = 0
    y = 0
    for dir in r:
        cmd = dir[0]
        dist = int(dir[1:])
        if cmd == 'L':
            for i in range(0, dist, 90):
                wp = [-wp[1], wp[0]]
        elif cmd == 'R':
            for i in range(0, dist, 90):
                wp = [wp[1], -wp[0]]
        elif cmd == 'F':
            dx, dy = wp
            x += dx * dist
            y += dy * dist
        else:
            dx, dy = mv[cmd]
            wp[0] += dx * dist
            wp[1] += dy * dist
    print(abs(x) + abs(y))


if __name__ == '__main__':
    day, year = 12, 2020
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
