from helpers.executor import Executor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from typing import Any, Callable, Generator, Sequence

day, year = 12, 2021
split_seq = '\n'


class Solution(Executor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        # if (len(r) > 10):
        #     return None

        edges = [set(sorted(q.split('-'))) for q in r]
        print(edges)
        #
        # for p in sorted(paths(edges, 'start', [])):
        #     print(','.join(p))

        return len(paths(edges, 'start', []))


    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        # TODO
        return None

def paths(edges, current: str, prev_nodes: list) -> list:
    if current == 'end':
        return [[current]]
    if current == 'start' and current in prev_nodes:
        return []
    if current == current.lower() and len(tuple(node for node in prev_nodes if node == node.lower())) != len(set(node for node in prev_nodes if node == node.lower())) and len(tuple(node for node in prev_nodes if node == current)) > 0:
        return []
    if current == current.lower() and len(tuple(node for node in prev_nodes if node == current)) > 1:
        return []
    # if len(tuple(node for node in prev_nodes if node == current)) > 1:
    #     return []

    prev_paths = []
    for edge in edges:
        if current in edge:
            other = next(iter(edge.difference((current,))))
            # if len(tuple(node for node in prev_nodes if node == other)) > (1 if current == current.upper() else 0):
            #     continue
            ps = paths(edges, other, prev_nodes + [current])
            for path in ps:
                # if len(tuple(node for node in prev_nodes if node == other)) > (1 if current == current.upper() else 0):
                #     continue
                prev_paths.append([current] + path)
    return prev_paths

if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
