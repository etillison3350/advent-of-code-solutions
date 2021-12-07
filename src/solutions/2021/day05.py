from helpers.executor import Executor

from helpers.util import *
import re
import numpy as np

from typing import Any, Callable, Generator, Sequence

day, year = 5, 2021
split_seq = '\n'


def sign(a):
    return 1 if a > 0 else (-1 if a < 0 else 0)


class Solution(Executor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        points = np.array([as_type(re.split('\\D+', s), int) for s in r])

        grid = np.zeros((np.max(points) + 1, np.max(points) + 1))

        for x1, y1, x2, y2 in points:
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            if x1 == x2:
                grid[x1, y1:y2+1] += 1
            elif y1 == y2:
                grid[x1:x2+1, y1] += 1

        return np.sum(grid > 1)

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        points = np.array([as_type(re.split('\\D+', s), int) for s in r])

        grid = np.zeros((np.max(points) + 1, np.max(points) + 1))

        for xa, ya, xb, yb in points:
            x1, x2 = min(xa, xb), max(xa, xb)
            y1, y2 = min(ya, yb), max(ya, yb)

            if x1 == x2:
                grid[x1, y1:y2 + 1] += 1
            elif y1 == y2:
                grid[x1:x2 + 1, y1] += 1
            else:
                for a in range(x2 - x1 + 1):
                    grid[xa + sign(xb - xa) * a, ya + sign(yb - ya) * a] += 1

        return np.sum(grid > 1)


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
