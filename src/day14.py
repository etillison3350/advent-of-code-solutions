from typing import Sequence

import input
from re import *


def get_addrs(mask: str, val: int):
    if 'X' not in mask:
        return [int(mask, 2) | val]
    else:
        fi = mask.index('X')
        return get_addrs(mask[:fi] + '0' + mask[fi+1:], val) + get_addrs(mask[:fi] + '1' + mask[fi+1:], val)


def run(r: Sequence[str]):
    mem = {}

    mask = 'X' * 36
    clr_mask = set_mask = 0
    for line in r:
        if line[1] == 'a':
            mask = line[7:]
            set_mask = int(mask.replace('X', '0'), 2)
            clr_mask = int(mask.replace('X', '1'), 2)
        else:
            cmd = search('\\[(\\d+)] = (\\d+)', line)
            addr = int(cmd.group(1))
            val = int(cmd.group(2))
            mem[addr] = (val & clr_mask) | set_mask
    print(sum([v for k, v in mem.items()]))

    mem = {}
    for line in r:
        if line[1] == 'a':
            mask = line[7:]
            set_mask = int(mask.replace('0', '1').replace('X', '0'), 2)
        else:
            cmd = search('\\[(\\d+)] = (\\d+)', line)
            addr = int(cmd.group(1)) & set_mask
            val = int(cmd.group(2))
            for a in get_addrs(mask, addr):
                mem[a] = val
    if len(mem) < 100:
        print(mem)
    print(sum([v for k, v in mem.items()]))


if __name__ == '__main__':
    day, year = 14, 2020
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
        print('Test case {}: {}'.format(index, str(tc_list)[:80]))
        try:
            run(tc_list)
        except Exception as ex:
            print('{}: {}'.format(type(ex).__name__, ex))
        finally:
            print('Done with test case {}'.format(index))
