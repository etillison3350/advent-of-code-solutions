from typing import Sequence

import input
from re import *

class llnode():
    def __init__(self, data, p=None, n=None):
        self.data = data
        self.p = p
        self.n = n

    def set_next(self, n):
        self.n = n
        n.p = self

    def set_prev(self, p):
        self.p = p
        p.n = self


def p(curr):
    a = [curr.data]
    cn = curr.n
    while cn != curr:
        a.append(cn.data)
        cn = cn.n
    return a


def run(r: Sequence[str]):
    cups = [int(k) for k in r[0]]
    max_cup = max(cups)

    head = llnode(cups[0])
    curr = head
    for c in cups[1:]:
        new = llnode(c)
        curr.set_next(new)
        curr = new
    curr.set_next(head)

    curr = head
    for k in range(100):
        cc = curr.data
        rem = curr.n
        curr.set_next(curr.n.n.n.n)

        t = cc
        cn = curr.p
        while True:
            t = (t - 2) % (max_cup) + 1
            while cn != curr:
                if cn.data == t:
                    break
                cn = cn.p
            if cn.data == t:
                break
            else:
                cn = cn.p
        rem.n.n.set_next(cn.n)
        cn.set_next(rem)
        curr = curr.n

    while curr.data != 1:
        curr = curr.n
    a = []
    cn = curr.n
    while cn != curr:
        a.append(cn.data)
        cn = cn.n
    print(''.join(str(k) for k in a))


if __name__ == '__main__':
    day, year = 23, 2020
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
