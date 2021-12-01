from typing import Sequence

from helpers import input


def run(r: Sequence[str]):
    products = [tuple(k.split(' (contains ')) for k in r]
    products = [(k.split(' '), v[:-1].split(', ')) for k, v in products]

    allergens = set()
    for _, a in products:
        allergens.update(a)
    algs = list(allergens)

    pos_map = {}
    for a in algs:
        pos_map[a] = set()

        for i, p in enumerate(products):
            if a not in p[1]:
                continue
            for ing in p[0]:
                for il, al in products[i + 1:]:
                    if a in al and ing not in il:
                        break
                else:
                    pos_map[a].add(ing)
            break

    alg_ings = set()
    for v in pos_map.values():
        alg_ings.update(v)

    ans = 0
    for il, _ in products:
        ans += len(set(il).difference(alg_ings))
    print(ans)

    alg_map = {}
    for _ in alg_ings:
        for k, v in pos_map.items():
            if len(v) == 1:
                alg_map[k] = next(iter(v))
                del pos_map[k]
                for v2 in pos_map.values():
                    v2.discard(alg_map[k])
                break
    print(','.join([v for _, v in sorted(list(alg_map.items()))]))


if __name__ == '__main__':
    day, year = 21, 2020
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
        # try:
        run(tc_list)
        # except Exception as ex:
        #     print('{}: {}'.format(type(ex).__name__, ex))
        # finally:
        #     print('Done with test case {}'.format(index))
