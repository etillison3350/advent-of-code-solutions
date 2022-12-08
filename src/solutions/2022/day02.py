from helpers.executor import SplitExecutor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from math import copysign

from typing import Any, Callable, Generator, Sequence

day, year = 2, 2022
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

        return sum(map(lambda q: {
            'A X': 4, 'A Y': 8, 'A Z': 3,
            'B X': 1, 'B Y': 5, 'B Z': 9,
            'C X': 7, 'C Y': 2, 'C Z': 6
        }[q], r))

    def _solve_part2(self, rs: tuple, print: Callable[..., None]) -> Any:
        r: Sequence[str]
        i: Sequence[int]
        n: np.ndarray

        r, i, n = rs

        return sum(map(lambda q: {
            'A X': 3, 'A Y': 4, 'A Z': 8,
            'B X': 1, 'B Y': 5, 'B Z': 9,
            'C X': 2, 'C Y': 6, 'C Z': 7
        }[q], r))


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
