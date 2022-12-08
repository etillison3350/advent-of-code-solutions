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

day, year = 8, 2022


class Solution(StrInputExecutor):
    def solve(self, r: ip.StrInput, print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def ct(self, val, slc):
        v = np.where(val <= slc)[0]
        if len(v) == 0:
            return len(slc)
        else:
            return v[0] + 1

    def sscore(self, arr, r, c):
        return self.ct(arr[r, c], arr[r - 1::-1, c]) \
               * self.ct(arr[r, c], arr[r, c - 1::-1]) \
               * self.ct(arr[r, c], arr[r + 1:, c]) \
               * self.ct(arr[r, c], arr[r, c + 1:])

    def visible(self, arr, r, c):
        return arr[r, c] > np.max([-1] + list(arr[:r,c])) \
               or arr[r, c] > np.max([-1] + list(arr[r,:c])) \
               or arr[r, c] > np.max([-1] + list(arr[r + 1:,c])) \
               or arr[r, c] > np.max([-1] + list(arr[r, c + 1:]))

    def _solve_part1(self, r: ip.StrInput, print: Callable[..., None]) -> Any:
        s = r.splitlines().list().int_list().np().native()

        total = 0
        for r in range(s.shape[0]):
            for c in range(s.shape[1]):
                if self.visible(s, r, c):
                    total += 1

        return total

    def _solve_part2(self, r: ip.StrInput, print: Callable[..., None]) -> Any:
        s = r.splitlines().list().int_list().np().native()

        max = 0
        for r in range(1, s.shape[0] - 1):
            for c in range(1, s.shape[1] - 1):
                ss = self.sscore(s, r, c)
                if ss > max:
                    max = ss

        return max


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(use_cached_test_cases=True)
