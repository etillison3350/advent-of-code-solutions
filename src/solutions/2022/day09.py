from helpers.executor import StrInputExecutor

import helpers.input_parse as ip

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from collections import defaultdict

from typing import Any, Callable, Generator

day, year = 9, 2022


class Solution(StrInputExecutor):
    def solve(self, r: ip.StrInput, print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: ip.StrInput, print: Callable[..., None]) -> Any:
        # s = r.splitlines().native()
        p = r.split('\n').sections().pd_records().drop_common().native_tuples()
        # g = r.grid_int(['\n', None])

        tpos = np.zeros(2)
        hpos = np.zeros(2)

        unique_pos = {(0, 0)}

        for d, n in p:
            offset = quict("L:10,R:12,U:01,D:21", val=lambda x: np.array([int(t) for t in x]) - 1)[d]

            for _ in range(n):
                hpos += offset
                if max(abs(tpos - hpos)) > 1:

                    tpos += np.sign((hpos - tpos) / 2) * np.ceil(np.abs((hpos - tpos) / 2))
                unique_pos.add(tuple(tpos.astype(int)))

        return len(unique_pos)

    def _solve_part2(self, r: ip.StrInput, print: Callable[..., None]) -> Any:
        p = r.split('\n').sections().pd_records().drop_common().native_tuples()
        # g = r.grid_int(['\n', None])

        pos = [np.zeros(2) for _ in range(10)]

        unique_pos = {(0, 0)}

        for d, n in p:
            offset = quict("L:10,R:12,U:01,D:21", val=lambda x: np.array([int(t) for t in x]) - 1)[d]

            for _ in range(n):
                pos[0] += offset
                for a, b in pairwise(range(10)):
                    assert b > a
                    if max(abs(pos[b] - pos[a])) > 1:
                        pos[b] += np.sign((pos[a] - pos[b]) / 2) * np.ceil(np.abs((pos[a] - pos[b]) / 2))
                unique_pos.add(tuple(pos[-1].astype(int)))

        return len(unique_pos)


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(use_cached_test_cases=True)
