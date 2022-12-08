from helpers.executor import SplitExecutor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from math import copysign

from typing import Any, Callable, Generator, Sequence

day, year = 4, 2022
split_seq = '\n'


class Solution(SplitExecutor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        rs = (
            r,
            [int(line) for line in r if re.fullmatch(r'^\d+$', line)],
            np.array(int(line) for line in r if re.fullmatch(r'^\d+$', line))
        )

        yield self._solve_part1(rs, print)
        yield self._solve_part2(rs, print)

    def _solve_part1(self, rs: tuple, print: Callable[..., None]) -> Any:
        r: Sequence[str]
        i: Sequence[int]
        n: np.ndarray

        r, i, n = rs

        ans = 0
        for line in r:
            x = [int(t) for t in re.split('\D+', line)]
            if x[0] <= x[2] and x[1] >= x[3]:
                ans += 1
            elif x[0] >= x[2] and x[1] <= x[3]:
                ans += 1

        return ans

    def _solve_part2(self, rs: tuple, print: Callable[..., None]) -> Any:
        r: Sequence[str]
        i: Sequence[int]
        n: np.ndarray

        r, i, n = rs

        ans = 0
        for line in r:
            x = [int(t) for t in re.split('\D+', line)]
            if len(set(range(x[0], x[1] + 1)).intersection(range(x[2], x[3] + 1))) > 0:
                ans += 1

        return ans


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
