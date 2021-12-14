from helpers.executor import Executor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from typing import Any, Callable, Generator, Sequence

day, year = 14, 2021
split_seq = '\n\n'


class Solution(Executor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        curr = r[0]

        pairs = dict([re.split('\\W+', s) for s in r[1].splitlines()])

        for n in range(10):
            new = ''
            for pair in itertools.pairwise(curr):
                if ''.join(pair) in pairs:
                    new += pair[0] + pairs[''.join(pair)]
            curr = new + curr[-1]
        print(curr)

        unique, counts = np.unique(list(curr), return_counts=True)

        ans = sorted(list(zip(counts, unique)))
        return ans[-1][0] - ans[0][0]


    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        curr = r[0]

        pairs = dict([re.split('\\W+', s) for s in r[1].splitlines()])

        unique, counts = np.unique(list(curr), return_counts=True)
        cts = dict(zip(unique, counts))

        unique, counts = np.unique(list(''.join(k) for k in itertools.pairwise(curr)), return_counts=True)
        curr = dict(zip(unique, counts))

        for n in range(40):
            new = {}
            for pair, count in curr.items():
                if pair in pairs:
                    new_sym = pairs[pair]
                    k1, k2 = new_sym + pair[1], pair[0] + new_sym
                    new[k1] = new.setdefault(k1, 0) + count
                    new[k2] = new.setdefault(k2, 0) + count
                    cts[new_sym] = cts.setdefault(new_sym, 0) + count
            curr = new

        print(curr)


        print(max(cts.values()) - min(cts.values()))

        return max(cts.values()) - min(cts.values())



if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
