import math

from helpers.executor import SplitExecutor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from typing import Any, Callable, Generator, Sequence

day, year = 9, 2021
split_seq = '\n'


class Solution(SplitExecutor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        grid = as_grid(r, int)

        ans = 0
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                min_val = math.inf
                for ax, ay in adj((x, y), diag=False):
                    if 0 <= ax < len(row) and 0 <= ay < len(grid):
                        min_val = min(grid[ay][ax], min_val)
                if col < min_val:
                    ans += col + 1
        return ans

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        grid = np.array(as_grid(r, int))

        basin_pts: set[tuple[Any, ...]] = set(zip(*np.where(grid < 9)))

        basins = []
        while len(basin_pts) > 0:
            basin_start = basin_pts.pop()
            basin = set()

            worklist = [basin_start]
            while len(worklist) > 0:
                co = worklist.pop()
                basin.add(co)
                for point in adj(co, diag=False):
                    if point in basin_pts:
                        worklist.append(point)
                        basin_pts.remove(point)
            basins.append(basin)
        return np.product(sorted((len(basin) for basin in basins), reverse=True)[:3])


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
