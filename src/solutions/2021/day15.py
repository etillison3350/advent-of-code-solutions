from helpers.executor import SplitExecutor

from helpers.util import *
import numpy as np
import heapq

from typing import Any, Callable, Generator, Sequence

day, year = 15, 2021
split_seq = '\n'


class Solution(SplitExecutor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        grid = np.array(as_grid(r, int))

        visited = set()
        stack = [(0, (0, 0))]
        while len(stack) > 0:
            cost, co = heapq.heappop(stack)
            if co in visited:
                continue
            visited.add(co)

            if co[0] == grid.shape[0] - 1 and co[1] == grid.shape[1] - 1:
                return cost

            for ax, ay in adj(co, False):
                if 0 <= ax < grid.shape[0] and 0 <= ay < grid.shape[1]:
                    heapq.heappush(stack, (cost + grid[ax, ay], (ax, ay)))

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        grid = np.array(as_grid(r, int)) - 1

        grid = np.vstack((grid, grid + 1, grid + 2, grid + 3, grid + 4))
        grid = (np.hstack((grid, grid + 1, grid + 2, grid + 3, grid + 4)) % 9) + 1

        visited = set()
        stack = [(0, (0, 0))]
        while len(stack) > 0:
            cost, co = heapq.heappop(stack)
            if co in visited:
                continue
            visited.add(co)

            if co[0] == grid.shape[0] - 1 and co[1] == grid.shape[1] - 1:
                return cost

            for ax, ay in adj(co, False):
                if 0 <= ax < grid.shape[0] and 0 <= ay < grid.shape[1]:
                    heapq.heappush(stack, (cost + grid[ax, ay], (ax, ay)))


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
