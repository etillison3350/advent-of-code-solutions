from helpers.executor import SplitExecutor

from helpers.util import *
import itertools
from itertools import *
import functools
from functools import *
import re
from re import *
import numpy as np
from math import ceil

from typing import Any, Callable, Generator, Sequence

day, year = 16, 2021
split_seq = '\n'


class Solution(SplitExecutor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        # if r[0] != '620080001611562C8802118E34':
        #     return
        if len(r[0]) < 100:
            while True:
                pass

        inp = ''.join('{:>04b}'.format(int(s, 16)) for s in r[0])

        return parse_packet(inp)



    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        # TODO
        return None


def parse_packet(pk: str):
    # print = lambda *x: None

    print(pk, len(pk))

    ver = int(pk[0:3], 2)
    typ = pk[3:6]

    if typ == '100':
        val = 0
        for n in range(6, len(pk), 5):
            val = 16 * val + int(pk[n+1:n+5], 2)
            if pk[n] == '0':
                # print('A', val, n + 5, ver)
                return val, n + 5, ver
    else:
        vals = []
        if pk[6] == '0':
            print(pk[7:22])
            ln = int(pk[7:22], 2) + 22
            s = 22
            while s < ln:
                # print('Sub t=0')
                v, l, vr = parse_packet(pk[s:])
                ver += vr
                vals.append(v)
                s += l
            # print('B', -2, ln, ver)
            # return -2, ln, ver
        else:
            n_pkts = int(pk[7:18], 2)
            s = 18
            for _ in range(n_pkts):
                # print('Sub t=1')
                v, l, vr = parse_packet(pk[s:])
                ver += vr
                vals.append(v)
                s += l
            # print('C', -1, s, ver)
            # return -1, s, ver
        if len(vals) < 2 and typ[0] == '1':
            print("ERR", pk, s)
            raise ValueError
        print(vals)
        return {
            '000': sum(vals),
            '001': reduce(lambda a, b: a * b, vals, 1),
            '010': min(vals),
            '011': max(vals),
            '101': 1 if len(vals) >= 2 and vals[0] > vals[1] else 0,
            '110': 1 if len(vals) >= 2 and vals[0] < vals[1] else 0,
            '111': 1 if len(vals) >= 2 and vals[0] == vals[1] else 0
        }[typ], s, ver


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
