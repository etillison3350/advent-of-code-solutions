from helpers.executor import SplitExecutor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from math import copysign

from typing import Any, Callable, Generator, Sequence

day, year = 5, 2022
split_seq = '\n\n'


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

        r, i, n = rs

        # if len(r[1]) > 100:
        #     return None

        q = np.array([list(line[1::4]) for line in r[0].splitlines()[:-1]]).T[:, ::-1]
        q = [[p for p in w if p != ' '] for w in q]
        print(q)

        for cmd in r[1].splitlines():
            _, count, src, dst = re.split(r'\D+', cmd)
            for _ in range(int(count)):
                q[int(dst) - 1].append(q[int(src) - 1].pop())
            # print(cmd, q)

        return ''.join([str(n[-1]) for n in q])

    def _solve_part2(self, rs: tuple, print: Callable[..., None]) -> Any:
        r: Sequence[str]
        i: Sequence[int]
        n: np.ndarray

        r, i, n = rs

        q = np.array([list(line[1::4]) for line in r[0].splitlines()[:-1]]).T[:, ::-1]
        q = [[p for p in w if p != ' '] for w in q]
        print(q)

        for cmd in r[1].splitlines():
            _, count, src, dst = re.split(r'\D+', cmd)
            q[int(dst) - 1].extend(q[int(src) - 1][-int(count):])
            q[int(src) - 1] = q[int(src) - 1][:-int(count)]
            # print(cmd, q)

        return ''.join([str(n[-1]) for n in q])


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
