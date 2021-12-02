from helpers.executor import Executor

from typing import Any, Callable, Generator, Sequence

day, year = 2, 2021  # TODO: Update day and year for current day
split_seq = '\n'


class Solution(Executor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        cmds = [(s[0], int(s[-1])) for s in r]

        x, y = 0, 0
        for dir, amt in cmds:
            if dir == 'f':
                x += amt
            elif dir == 'd':
                y += amt
            else:
                y -= amt

        return x * y

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        cmds = [(s[0], int(s[-1])) for s in r]

        aim, x, y = 0, 0, 0
        for d, amt in cmds:
            if d == 'f':
                x += amt
                y += amt * aim
            elif d == 'd':
                aim += amt
            else:
                aim -= amt

        return x * y


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
