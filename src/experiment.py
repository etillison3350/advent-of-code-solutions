from helpers.input_parse import *

from helpers.util import *

from helpers.input_parse.inference import JointInference, GridInference

import numpy as np

import os

import timeit

from collections import Counter

if __name__ == '__main__':
    with open(r'..\src\inputs\2020\input-202016.txt', 'r') as file:
        t = file.read()
    s = StrInput(t)

    r = []

    dir = r'.\inputs'
    for dirpath, dirnames, filenames in os.walk(dir):
        for file in filenames:
            if file.startswith('input'):
                with open(os.path.join(dirpath, file), 'r') as inp_file:
                    t = inp_file.read()

    #             print(file)
    #             results = [
    #                 # timeit.timeit(lambda: Counter(t), number=1000),
    #                 timeit.timeit(lambda: {c: t.count(c) for c in set(t)}, number=1000),
    #                 timeit.timeit(lambda: set(t), number=1000)
    #             ]
    #
    #             print(results[1] / results[0])
    #
    #             # print('Counter:', results[0])
    #             # print('count:', results[1])
    #
    #             r.append(results[1] / results[0])
    # print(sum(r) / len(r))


                # if '\n' in t:
                #     print(file, ':', t.count('\n'), len(t), t.count('\n') / len(t))
                #     maxchar = max((c for c in set(t) if c != '\n'), key=t.count)
                #     print(' ' * len(file), maxchar, t.count(maxchar), len(t), t.count(maxchar) / len(t))

                j = JointInference(StrInput(t), 'r')
                # j = GridInference(StrInput(t), 'r')
                if j.is_valid():
                    print(file)
                    print(*t.splitlines()[:4], sep='\n')
                    for s in j.get_expr(max_alts=10):
                        lines = s.splitlines()
                        for line in lines:
                            print('\t', line)
                        if len(lines) > 1:
                            print()


    # print(alph_map())

    # print(s.grid_int(['\n', ',']))

    # print(s.grid(cvt=quict('1:a, 2:b, 3:c, 4:d, 5:e')).native())

    # print(adj_np(np.zeros(5)))

    # q = quict('a:01, b:10, c:4, d: 125', val=tuple)
    # print(q)

    # print(s.splitlines().list().opt_int().np().native())

    # print(s.split_paragraphs()[1:].sections().pd_records().drop_common().native())

    # print(s.splitlines().sections('A-Za-z', '0-9+-').pd_records().drop_common().native())

    # print(s.splitlines()[2:].sections().strip().pd_records().drop_common().native())

    # print(s.sections().filter_type(int).native())

    # print(s.split(',').sections().native())

    # print(s.splitlines().list().native())

    # print(s.splitlines().split(r'\s+', remove_empty=True).opt_int().np().native())

    # print(s.splitlines().sections('a-z-', '0-9', opt_int=False).split('-').flat().opt_int().pd_records().drop_common().native_tuples())

    # print(s.splitlines().extract(r'\[[a-z]+\]').native())

    # print(s.json())
    # a, b = s.split_paragraphs()
    # print(a.splitlines().sections().split('(?=[A-Z])', remove_empty=True).pd_records().drop_common().tuples().native())
