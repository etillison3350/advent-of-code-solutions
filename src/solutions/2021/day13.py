from helpers.executor import Executor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from typing import Any, Callable, Generator, Sequence

day, year = 13, 2021
split_seq = '\n\n'


class Solution(Executor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        points, folds = r
        points = points.split('\n')
        folds = folds.split('\n')

        grid = np.zeros((10000, 10000))
        for point in points:
            x, y = point.split(',')
            grid[int(x), int(y)] = 1

        for fold in folds:
            dir = 'x' if 'x' in fold else 'y'
            line = int(fold.split('=')[-1])

            if dir == 'x':
                for n in range(1, 10000):
                    if line - n < 0 or line + n >= 10000:
                        break
                    grid[line - n, :] += grid[line + n, :]
                    grid[line + n, :] = 0
            else:
                for n in range(1, 10000):
                    if line - n < 0 or line + n >= 10000:
                        break
                    grid[:, line - n] += grid[:, line + n]
                    grid[:, line + n] = 0
            print(grid[:40, :6])
            print(len(np.where(grid > 0)[0]))
            print(chr(len(np.where(grid > 0)[0]) & 0x7F))
        print((grid[:40, :6].T > 0).astype(int))
        return len(np.where(grid > 0)[0])

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        pass


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
