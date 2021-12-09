import math

from helpers.executor import Executor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from typing import Any, Callable, Generator, Sequence

day, year = 9, 2021
split_seq = '\n'


class Solution(Executor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        g = as_grid(r, int)
        n = 0

        for y, row in enumerate(g):
            for x, col in enumerate(row):
                m = math.inf
                for ax, ay in adj((x, y)):
                    if (ax == x or ay == y) and 0 <= ax < len(row) and 0 <= ay < len(g):
                        m = min(g[ay][ax], m)
                if col < m:
                    n += g[y][x] + 1
        return n

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        g = np.array(as_grid(r, int))

        basin_pts: set[tuple[Any, ...]] = set(zip(*np.where(g < 9)))

        basins = []
        while len(basin_pts) > 0:
            basin_start = basin_pts.pop()
            basin = set()

            wl = [basin_start]
            while len(wl) > 0:
                co = wl.pop()
                basin.add(co)
                for ax, ay in adj(co):
                    if (ax == co[0] or ay == co[1]) and (ax, ay) in basin_pts:
                        wl.append((ax, ay))
                        basin_pts.remove((ax, ay))
            basins.append(basin)
        return np.product(sorted((len(basin) for basin in basins), reverse=True)[:3])



if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
