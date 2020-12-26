from typing import Sequence

import input


def run(r: Sequence[str]):
    pk1, pk2 = (int(k) for k in r)

    cv = 1
    sn = 7
    ln = 0
    while cv != pk1:
        ln += 1
        cv *= sn
        cv %= 20201227
    print(ln)

    sn = pk2
    cv = 1
    for _ in range(ln):
        cv *= sn
        cv %= 20201227
    print(cv)


if __name__ == '__main__':
    day, year = 25, 2020
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
