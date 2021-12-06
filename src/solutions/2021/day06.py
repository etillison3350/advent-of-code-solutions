from helpers.executor import Executor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *

from typing import Any, Callable, Generator, Sequence

import numpy as np

day, year = 6, 2021
split_seq = ','


class Solution(Executor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve(r, 80)
        yield self._solve(r, 256)

    def _solve(self, r: Sequence[str], n) -> Any:
        timers = np.zeros(10)
        unique, counts = np.unique(as_type(r, int), return_counts=True)
        timers[unique] = counts

        for _ in range(n):
            timers[7] += timers[0]
            timers[9] += timers[0]
            timers = np.roll(timers, -1)
            timers[-1] = 0
        return np.sum(timers)


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
