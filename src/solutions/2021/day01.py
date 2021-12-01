from typing import Any, Callable, Generator, Sequence

from helpers.executor import Executor

from helpers.util import *
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
        k = as_type(r, int)
        return sum(b > a for a, b in itertools.pairwise(k))

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        k = as_type(r, int)
        sums = [sum(part) for part in nwise(k, 3)]
        return sum(b > a for a, b in itertools.pairwise(sums))


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
