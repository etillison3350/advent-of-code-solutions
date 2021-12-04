from typing import Any, Callable, Generator, Optional, Sequence

from datetime import date

from functools import partial
import io

from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
from helpers import input


class Executor:
    def __init__(self, year: Optional[int] = None, day: Optional[int] = None):
        today = date.today()

        self.year = year if year is not None else today.year
        self.day = day if day is not None else today.day

        if self.year < 2000:
            raise ValueError('Sanity: year should be at least 2000')
        if self.day < 1 or self.day > 25:
            raise ValueError('Sanity: day should be between 1 and 25')

    def solve(self, input_lines: Sequence[str], print: Callable[..., None]) -> Generator[Any, None, None]:
        pass

    def _compute_true_output(self, input_lines: Sequence[str], output_pipe: Connection) -> None:
        answers = []

        for ans in self.solve(input_lines, print):
            answers.append(ans)
            print('---- True Output ----',
                  *['Ans. #{}:\n{}'.format(part + 1, a) for part, a in enumerate(answers)],
                  sep='\n', end='\n\n')
            output_pipe.send(ans)
        output_pipe.close()

    def _compute_test_cases(self, test_cases: Sequence[str], split_seq: str, true_output_pipe: Connection) -> None:
        true_answers = []

        for index, tc in enumerate(test_cases):
            tc_list = tc.split(split_seq)
            tc_str = str(tc_list)

            # Save all test-case output into a list to be printed all at once
            tc_output = io.StringIO()
            print('---- Test case {}: {}{} ----'.format(index, tc_str[:80], '...' if len(tc_str) > 80 else ''),
                  file=tc_output)

            tc_print = partial(print, file=tc_output)

            try:
                # Run the test case
                for part, ans in enumerate(self.solve(tc_list, tc_print)):
                    print('Test Ans. #{}:\n{}'.format(part + 1, ans), file=tc_output)
            except Exception as ex:
                # Print any errors
                print('{}: {}'.format(type(ex).__name__, ex), file=tc_output)
            finally:
                print('Done with test case {}\n'.format(index), file=tc_output)

            # If we've received any true output during this output, print it too (so we don't miss it)
            while true_output_pipe.poll():
                true_answers.append(true_output_pipe.recv())

            if len(true_answers) > 0 and any(ans is not None for ans in true_answers):
                print('---- True Output ----',
                      *['Ans. #{}:\n{}'.format(part + 1, a) for part, a in enumerate(true_answers) if a is not None],
                      sep='\n', end='\n\n', file=tc_output)

            print(tc_output.getvalue())
            tc_output.close()

        true_output_pipe.close()

    def execute(self, split_seq: str = '\n', use_cached_test_cases=True):
        input.wait_for_input(self.day, self.year)

        recv_pipe, send_pipe = Pipe(False)

        inp = input.input_text(self.day, self.year)
        input_lines = inp.split(split_seq)

        true_output_proc = Process(target=self._compute_true_output, args=(input_lines, send_pipe))
        true_output_proc.start()

        test_cases = input.find_test_cases(self.day, self.year, cached=use_cached_test_cases)
        test_case_proc = Process(target=self._compute_test_cases, args=(test_cases, split_seq, recv_pipe))
        test_case_proc.start()

        true_output_proc.join()
        test_case_proc.join()
