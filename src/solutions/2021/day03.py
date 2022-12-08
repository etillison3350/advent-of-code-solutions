from helpers.executor import SplitExecutor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *

import numpy as np

from typing import Any, Callable, Generator, Sequence

day, year = 3, 2021
split_seq = '\n'


class Solution(SplitExecutor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        ns = np.array([[int(k) for k in s] for s in r])
        bits = np.sum(ns, axis=0)
        f = int(''.join([str(x) for x in (bits > len(ns) / 2).astype(int)]), 2)
        return f * ((~f) & ((1 << ns.shape[1]) - 1))

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        ns = np.array([[int(k) for k in s] for s in r])
        bits = np.sum(ns, axis=0)
        f = (bits > len(ns) // 2).astype(int)
        g = 1 - f

        nsp = ns.copy()
        for x in range(ns.shape[1]):
            if np.any(nsp[:, x] == f[x]):
                nsp = nsp[np.where(nsp[:, x] == f[x])].astype(int)
            else:
                break
            print(nsp)
            if len(nsp) == 1:
                break
            bits = np.sum(nsp, axis=0)
            f = (bits >= len(nsp) / 2).astype(int)
            print(f)

        nsq = ns.copy()
        for x in range(ns.shape[1]):
            if np.any(nsq[:, x] == g[x]):
                nsq = nsq[np.where(nsq[:, x] == g[x])].astype(int)
            else:
                break
            print(nsq)
            if len(nsq) == 1:
                break
            bits = np.sum(nsq, axis=0)
            g = 1 - (bits >= len(nsq) / 2).astype(int)
            print(f)

        a = int(''.join([str(x) for x in nsq.astype(int)[0]]), 2)
        b = int(''.join([str(x) for x in nsp.astype(int)[0]]), 2)
        print(a, b)
        return a * b


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
