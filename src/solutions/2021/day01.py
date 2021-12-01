from typing import Any, Callable, Generator, Sequence

from helpers.executor import Executor

import itertools
from itertools import *
import re
from re import *

day, year = 1, 2021
split_seq = '\n'


class Solution(Executor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        k = [int(v) for v in r]
        ans = 0
        for i in range(1, len(k)):
            if k[i] > k[i - 1]:
                ans += 1
        return ans

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        k = [int(v) for v in r]
        ans = 0

        s = []

        for i in range(3, len(k) + 1):
            s.append(sum(k[i - 3:i]))

        for i in range(1, len(s)):
            if s[i] > s[i - 1]:
                ans += 1

        return ans


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
