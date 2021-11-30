from typing import Sequence

import input
from re import *
import re


def run(r: Sequence[str]):
    sum = 0
    for eq in r:
        eq = '({})'.format(eq.replace(' ', ''))
        while True:
            par = search('\\([^()]+\\)', eq)
            if par is None:
                break
            expr = re.split('(?=[+*])', '+' + par.group()[1:-1])[1:]
            val = 0
            for term in expr:
                op = term[0]
                n = int(term[1:])
                if op == '+':
                    val += n
                else:
                    val *= n
            eq = eq[:par.start()] + str(val) + eq[par.end():]
        sum += int(eq)
    print(sum)

    sum = 0
    for eq in r:
        eq = '({})'.format(eq.replace(' ', ''))
        while True:
            par = search('\\([^()]+\\)', eq)
            if par is None:
                break
            expr = par.group()[1:-1]
            while True:
                add = search('(\\d+)\\+(\\d+)', expr)
                if add is None:
                    break
                add1, add2 = int(add.group(1)), int(add.group(2))
                expr = expr[:add.start()] + str(add1 + add2) + expr[add.end():]
            expr = re.split('(?=\\*)', '*' + expr)[1:]
            val = 1
            for term in expr:
                n = int(term[1:])
                val *= n
            eq = eq[:par.start()] + str(val) + eq[par.end():]
        sum += int(eq)
    print(sum)


if __name__ == '__main__':
    day, year = 18, 2020
    input.wait_for_input(day, year)

    split_seq = '\n'

    inp = input.input_text(day, year)
    input_lines = inp.split(split_seq)

    print('True output:')
    run(input_lines)
    print()

    print('Possible test cases:')
    test_cases = input.find_test_cases(day, year, cached=True)
    for index, tc in enumerate(test_cases):
        tc_list = tc.split(split_seq)
        tc_str = str(tc_list)
        print('Test case {}: {}{}'.format(index, tc_str[:80], '...' if len(tc_str) > 80 else ''))
        try:
            run(tc_list)
        except Exception as ex:
            print('{}: {}'.format(type(ex).__name__, ex))
        finally:
            print('Done with test case {}'.format(index))
