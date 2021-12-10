from helpers.executor import Executor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from typing import Any, Callable, Generator, Sequence

day, year = None, None  # TODO: Update day and year for current day
split_seq = '\n'


class Solution(Executor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        cm = {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137
        }

        open, close = '([{<', ')]}>'
        ans = 0
        for line in r:
            st = []
            for char in line:
                if char in open:
                    st.append(char)
                elif open.index(st.pop()) != close.index(char):
                    ans += cm[char]
        return ans

        # ans = 0
        # cts = [0] * 4
        # for line in r:
        #     for char in line:
        #         if char in '([{<':
        #             cts['([{<'.index(char)] += 1
        #         else:
        #             cts[')]}>'.index(char)] -= 1
        #             if cts[')]}>'.index(char)] < 0:
        #                 ans += cm[char]
        #                 break
        # return ans

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        open, close = '([{<', ')]}>'
        scores = []
        for line in r:
            st = []
            for char in line:
                if char in open:
                    st.append(char)
                elif open.index(st.pop()) != close.index(char):
                    break
            else:
                n = 0
                while len(st) > 0:
                    c = st.pop()
                    n = n * 5 + open.index(c) + 1
                scores.append(n)
        return sorted(scores)[len(scores) // 2]


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
