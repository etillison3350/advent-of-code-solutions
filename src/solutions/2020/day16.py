from typing import Sequence

from helpers import input
from re import *


def assign(l: Sequence[set]):
    if len(l) == 1:
        if len(l[0]) == 1:
            return {0: l[0].pop()}
        return None
    for p in l[-1]:
        a = assign([s - {p} for s in l[:-1]])
        if a:
            a[len(l) - 1] = p
            return a
    return None


def run(r: Sequence[str]):
    fields = [search('([\\w\\s]+): (\\d+)-(\\d+) or (\\d+)-(\\d+)', fld) for fld in r[0].splitlines()]
    fields = {s.group(1): (int(s.group(2)), int(s.group(3)), int(s.group(4)), int(s.group(5))) for s in fields}
    your_ticket = [int(k) for k in r[1].splitlines()[1].split(',')]
    other_tickets = [[int(k) for k in row.split(',')] for row in r[2].splitlines()[1:]]

    valid_tickets = []

    ans = 0
    for o in other_tickets:
        for n in o:
            for l1, u1, l2, u2 in fields.values():
                if n in range(l1, u1 + 1) or n in range(l2, u2 + 1):
                    break
            else:
                break
        else:
            valid_tickets.append(o)
    print(ans)

    pos = [set(fields.keys()) for _ in range(len(fields))]
    for ticket in valid_tickets:
        for ix, fld_val in enumerate(ticket):
            pos_flds = pos[ix]
            impos = set()
            for fn in pos_flds:
                l1, u1, l2, u2 = fields[fn]
                if fld_val not in range(l1, u1 + 1) and fld_val not in range(l2, u2 + 1):
                    impos.add(fn)
            pos[ix] = pos_flds.difference(impos)
    print(pos)

    a = assign(pos)
    print(a)

    ans = 1
    for ix, k in a.items():
        print(k + ': ' + str(your_ticket[ix]))
        if k[0:9] == 'departure':
            ans *= your_ticket[ix]
    print(ans)

    # ans = 1
    #
    # possible_assignments = product(*pos)
    # for a in possible_assignments:
    #     if set(a) == set(fields.keys()):
    #         print(a)
    #         for i, k in enumerate(a):
    #             print(k + ': ' + str(yt[i]))
    #             if k[0:9] == 'departure':
    #                 ans *= yt[i]
    #         print(ans)
    #         break


if __name__ == '__main__':
    day, year = 16, 2020
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
