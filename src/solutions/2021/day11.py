from helpers.executor import SplitExecutor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from typing import Any, Callable, Generator, Sequence

day, year = 11, 2021
split_seq = '\n'


class Solution(SplitExecutor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        s = np.array(as_grid(r, int))

        n_flash = 0
        for _ in range(100):
            s += 1

            flashed = np.zeros_like(s)
            while True:
                flashes = list(zip(*np.where((s > 9) * (flashed == 0))))
                flashed[np.where(s > 9)] = 1
                if len(flashes) == 0:
                    break
                n_flash += len(flashes)

                for co in flashes:
                    for ax, ay in adj(co, True):
                        if 0 <= ax < s.shape[0] and 0 <= ay < s.shape[1]:
                            s[ax][ay] += 1
            s[s > 9] = 0
        return n_flash

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        s = np.array(as_grid(r, int))

        k = 0
        while True:
            k += 1
            s += 1
            flashed = np.zeros_like(s)
            while True:
                flashes = list(zip(*np.where((s > 9) * (flashed == 0))))
                flashed[np.where(s > 9)] = 1
                if len(flashes) == 0:
                    break

                for co in flashes:
                    for ax, ay in adj(co, True):
                        if 0 <= ax < s.shape[0] and 0 <= ay < s.shape[1]:
                            s[ax][ay] += 1
            s[s > 9] = 0

            if np.all(flashed):
                return k


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
