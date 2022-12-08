from helpers.executor import SplitExecutor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from math import copysign

from typing import Any, Callable, Generator, Sequence

day, year = 3, 2022
split_seq = '\n'


class Solution(SplitExecutor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        rs = (
            r,
            [int(line) for line in r if re.fullmatch(r'^\d+$', line)],
            np.array(int(line) for line in r if re.fullmatch(r'^\d+$', line))
        )

        yield self._solve_part1(rs, print)
        yield self._solve_part2(rs, print)

    def _solve_part1(self, rs: tuple, print: Callable[..., None]) -> Any:
        r: Sequence[str]
        i: Sequence[int]
        n: np.ndarray

        a, i, n = rs

        b = [(x[:len(x) // 2], x[len(x) // 2:]) for x in a]
        c = [(set(x), set(y)) for x, y in b]
        d = [x.intersection(y) for x, y in c]
        e = [ord(next(iter(x))) for x in d]
        f = [((x - 38) if (x < 94) else (x - 96)) for x in e]
        return sum(f)

    def _solve_part2(self, rs: tuple, print: Callable[..., None]) -> Any:
        r: Sequence[str]
        i: Sequence[int]
        n: np.ndarray

        a, i, n = rs

        b = list(zip(a[0::3], a[1::3], a[2::3]))
        c = [(set(x), set(y), set(z)) for x, y, z in b]
        d = [x.intersection(y).intersection(z) for x, y, z in c]
        e = [ord(next(iter(x))) for x in d]
        f = [((x - 38) if (x < 94) else (x - 96)) for x in e]
        return sum(f)


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
