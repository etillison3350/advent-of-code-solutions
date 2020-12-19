from typing import Sequence

import input
from re import *
from itertools import product


memo = {}


def get_cfg_values(cfg: dict, rule: int):
    if rule in memo:
        return memo[rule]
    r = cfg[rule]
    if isinstance(r, str):
        memo[rule] = {r}
        return {r}
    ret = set()
    for opt in r:
        ret.update({''.join(l) for l in product(*[get_cfg_values(cfg, n) for n in opt])})
    memo[rule] = ret
    return ret


def run(r: Sequence[str]):
    global memo
    memo = {}

    rules, msgs = r
    rule_map = {}
    for rule in rules.splitlines():
        rs = search('(\\d+): (?:"(.+?)"|([\\d |]+))', rule)
        rule_map[int(rs.group(1))] = rs.group(2) or [[int(k) for k in g.split(' ')] for g in rs.group(3).split(' | ')]

    msgs = set(msgs.splitlines())
    valid_values = get_cfg_values(rule_map, 0)
    valid_msgs = list(msgs.intersection(valid_values))
    print(len(valid_msgs))

    invalid_msgs = msgs.difference(valid_values)

    re = '((?:' + '|'.join(memo[42]) + ')+)' + '((?:' + '|'.join(memo[31]) + ')+)'
    len42 = len(next(iter(memo[42])))
    len31 = len(next(iter(memo[31])))
    for m in invalid_msgs:
        rs = fullmatch(re, m)
        if rs is not None and len(rs.group(1)) / len42 > len(rs.group(2)) / len31:
            valid_msgs.append(m)
    print(len(valid_msgs))


if __name__ == '__main__':
    day, year = 19, 2020
    input.wait_for_input(day, year)

    split_seq = '\n\n'

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
