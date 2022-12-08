from helpers.input_parse import *

from helpers.util import *

import numpy as np

if __name__ == '__main__':
    with open(r'C:\Users\ethan\Documents\Programming\AdventOfCode\Solutions\src\inputs\2018\input-201825.txt', 'r') as file:
        t = file.read()
    s = StrInput(t)

    # print(alph_map())

    print(s.grid_int(['\n', ',']))

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
