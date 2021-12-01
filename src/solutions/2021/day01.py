from typing import Any, Callable, Generator, Sequence

from helpers.executor import Executor

import itertools
import re
from re import *

day, year = 1, 2021
split_seq = '\n'


class Solution(Executor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        # TODO
        return None

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        # TODO
        return None


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
