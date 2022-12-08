from helpers.executor import SplitExecutor

from helpers.util import *
import itertools
from itertools import *
import re
from re import *
import numpy as np

from typing import Any, Callable, Generator, Sequence

day, year = 8, 2021
split_seq = '\n'


class Solution(SplitExecutor):
    def solve(self, r: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        yield self._solve_part1(r, print)
        yield self._solve_part2(r, print)

    def _solve_part1(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        lines = [line.split(' | ') for line in r]
        ans = 0
        for _, output_value in lines:
            for part in output_value.split():
                if len(part) in (2, 3, 4, 7):
                    ans += 1
        return ans

    def _solve_part2(self, r: Sequence[str], print: Callable[..., None]) -> Any:
        # Which segments are on for each digit?
        # Segments are numbered left-to-right:
        #  0
        # 1 2
        #  3
        # 4 5
        #  6
        segment_map = [
            {0, 1, 2, 4, 5, 6},     # 0
            {2, 5},                 # 1
            {0, 2, 3, 4, 6},        # 2
            {0, 2, 3, 5, 6},        # 3
            {1, 2, 3, 5},           # 4
            {0, 1, 3, 5, 6},        # 5
            {0, 1, 3, 4, 5, 6},     # 6
            {0, 2, 5},              # 7
            {0, 1, 2, 3, 4, 5, 6},  # 8
            {0, 1, 2, 3, 5, 6}      # 9
        ]

        # Map from number of active segments (word length in input) to digits with that many active segments
        length_map = [{index for index, s in enumerate(segment_map) if len(s) == n} for n in range(2, 8)]

        # In a list sorted by word length, these are all possible orders of the digits
        digit_orderings = set(sum(p, start=()) for p in itertools.product(*(itertools.permutations(v) for v in length_map)))

        lines = [line.split(' | ') for line in r]
        ans = 0
        for input_values, output_values in lines:
            # Sort the words in the input section by length. Also sort the characters in each word
            input_words = sorted((sorted(word) for word in input_values.split()), key=lambda x: len(x))

            # Find the order of the digits that produces a valid mapping from letter to segment index
            for order in digit_orderings:
                # Possible letters corresponding to each of the seven segments
                possible_segs = [set('abcdefg') for _ in range(7)]

                # Remove impossible letters from possible_segs by set intersection
                for word, digit in zip(input_words, order):
                    for ix in segment_map[digit]:
                        possible_segs[ix].intersection_update(set(word))
                # This mapping is valid only if there is at least one possible letter for each segment
                if all(len(s) > 0 for s in possible_segs):
                    # The four digit number in the output
                    num = 0
                    for word in output_values.split():
                        # Find the word in the input, and use that to index into the digit order to get the digit
                        # represented by this word (note that the characters in the word are sorted so that dbac = cbad)
                        digit = order[input_words.index(sorted(word))]
                        num = 10 * num + digit
                    ans += num
                    break
        return ans


if __name__ == '__main__':
    solution = Solution(year, day)
    solution.execute(split_seq, use_cached_test_cases=True)
