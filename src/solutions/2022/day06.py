from helpers.executor import SplitExecutor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from math import copysign

from typing import Any, Callable, Generator, Sequence

day, year = 6, 2022
split_seq = '\n\n'


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
        n: np.ndarray

        r, _, n = rs

        q = r[0]
        for i in range(4, len(q)):
            if len(set(q[i - 4:i])) == 4:
                return i

    def _solve_part2(self, rs: tuple, print: Callable[..., None]) -> Any:
        r: Sequence[str]
        n: np.ndarray

        r, _, n = rs

        q = r[0]
        for i in range(14, len(q)):
            if len(set(q[i - 14:i])) == 14:
                return i




if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
