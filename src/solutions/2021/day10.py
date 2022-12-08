from helpers.executor import SplitExecutor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from typing import Any, Callable, Generator, Sequence

day, year = 10, 2021
split_seq = '\n'


class Solution(SplitExecutor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        character_values = {')': 3, ']': 57, '}': 1197, '>': 25137}

        open_parens, close_parens = '([{<', ')]}>'
        ans = 0
        for line in r:
            stack = []
            for char in line:
                if char in open_parens:
                    stack.append(char)
                elif open_parens.index(stack.pop()) != close_parens.index(char):
                    ans += character_values[char]
        return ans

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        open_parens, close_parens = '([{<', ')]}>'
        scores = []
        for line in r:
            stack = []
            for char in line:
                if char in open_parens:
                    stack.append(char)
                elif open_parens.index(stack.pop()) != close_parens.index(char):
                    break
            else:
                n = 0
                while len(stack) > 0:
                    c = stack.pop()
                    n = n * 5 + open_parens.index(c) + 1
                scores.append(n)
        return sorted(scores)[len(scores) // 2]


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
