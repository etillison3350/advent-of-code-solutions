import math

from helpers.executor import Executor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from typing import Any, Callable, Generator, Sequence

day, year = 7, 2021
split_seq = ','


class Solution(Executor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        s = np.array(as_type(r, int))

        min = (None, math.inf)
        for x in range(0, max(s)):
            if np.sum(np.abs(s - x)) < min[1]:
                min = (x, np.sum(np.abs(s - x)))
        return min[1]

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        s = np.array(as_type(r, int))

        min = (None, math.inf)
        for x in range(0, max(s)):
            d = np.abs(s - x)
            if np.sum(d * (d + 1) / 2) < min[1]:
                min = (x, np.sum(d * (d + 1) / 2))
        return min


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
