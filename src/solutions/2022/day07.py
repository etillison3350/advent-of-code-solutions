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

day, year = 7, 2022


class Solution(StrInputExecutor):
    def solve(self, r: ip.StrInput, print: Callable[..., None]) -> Generator[Any, None, None]:
        s = r.splitlines().native()
        # p = r.split('\n').sections().pd_records().drop_common().native()

        m = defaultdict(list)
        curr_path = []
        for i in range(len(s)):
            line = s[i]
            if line[0:4] == '$ cd':
                if line[5:7] == '..':
                    curr_path.pop()
                else:
                    curr_path.append(line[5:])
            elif line == '$ ls':
                j = i + 1
                while j < len(s) and s[j][0] != '$':
                    j += 1
                files = s[i + 1:j]
                for file in files:
                    if file[0:3] != 'dir':
                        m[tuple(curr_path)].append(int(file.split(' ')[0]))

        print(m)

        dirs = defaultdict(int)
        for path, sizes in m.items():
            for d in range(1 + len(path)):
                dirs[path[0:d]] += sum(sizes)

        print(dirs)

        yield sum(d for _, d in dirs.items() if d < 100000)

        current = dirs[('/', )]
        free = 70000000 - current
        needed = 30000000 - free
        yield min(d for _, d in dirs.items() if d > needed)


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(use_cached_test_cases=True)
