from helpers.executor import Executor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from typing import Any, Callable, Generator, Sequence

day, year = 8, 2021
split_seq = '\n'


class Solution(Executor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        s = [re.split(' \| ', sr) for sr in r]
        n = 0
        for _, ov in s:
            for part in ov.split():
                if len(part) in (2, 3, 4, 7):
                    n += 1
        return n

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        segment_map = [
            'abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg'
        ]
        sm = [set(ord(c) - 97 for c in s) for s in segment_map]

        dm = {
            2: {1},
            3: {7},
            4: {4},
            5: {2, 3, 5},
            6: {0, 6, 9},
            7: {8}
        }
        qm = {}
        for d, st in dm.items():
            qm[d] = set()
            for n in st:
                qm[d].update(sm[n])

        do = set(sum(p, start=()) for p in itertools.product(*(itertools.permutations(v) for v in dm.values())))

        s = [re.split(' \| ', sr) for sr in r]
        n = 0
        for iv, ov in s:
            ds = sorted(iv.split(), key=lambda x: len(x))
            for order in do:
                possible_segs = [set('abcdefg') for _ in range(7)]

                for sigs, dig in zip(ds, order):
                    pd = sm[dig]
                    for ix in pd:
                        possible_segs[ix].intersection_update(set(sigs))
                if all(len(x) > 0 for x in possible_segs):
                    print(possible_segs)
                    while not all(len(x) == 1 for x in possible_segs):
                        singles = set()
                        for x in possible_segs:
                            if len(x) == 1:
                                singles.update(x)
                        for x in possible_segs:
                            if len(x) > 1:
                                x.difference_update(singles)
                    print(possible_segs)
                    num = 0
                    for part in ov.split():
                        ssd = set()

                        for i, s in enumerate(possible_segs):
                            if next(iter(s)) in part:
                                ssd.add(i)
                        f = [i for i, st in enumerate(sm) if st == ssd][0]
                        num = 10 * num + f
                    print(num)
                    n += num
                    break
        return n


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
