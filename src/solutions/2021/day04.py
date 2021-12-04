from helpers.executor import Executor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *

import numpy as np

from typing import Any, Callable, Generator, Sequence

day, year = 4, 2021
split_seq = '\n\n'


class Solution(Executor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        numbers = as_type(r[0].split(','), int)
        boards = r[1:]
        boards = np.array([[as_type(re.split(' +', row.strip()), int) for row in b.split('\n')] for b in boards])

        matches = np.zeros_like(boards)

        for n in numbers:
            matches[boards == n] = 1

            for a in range(1, 3):
                wins = np.sum(matches, axis=a) == 5
                if np.any(wins):
                    wb = np.where(wins)[0]

                    return np.sum(boards[wb] * (1 - matches[wb])) * n


    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        numbers = as_type(r[0].split(','), int)
        boards = r[1:]
        boards = np.array([[as_type(re.split(' +', row.strip()), int) for row in b.split('\n')] for b in boards])

        matches = np.zeros_like(boards)

        prev_wins = None
        for n in numbers:
            matches[boards == n] = 1

            wins_1, wins_2 = np.sum(matches, axis=1) == 5, np.sum(matches, axis=2) == 5
            aw = wins_1.sum(axis=1) + wins_2.sum(axis=1)
            if np.all(aw > 0):
                wb = np.where(prev_wins == 0)[0]

                return np.sum(boards[wb] * (1 - matches[wb])) * n
            prev_wins = aw


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
