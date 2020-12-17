from itertools import product

def adj(co):
    d = len(co)
    return {tuple(a[i] + co[i] for i in range(d)) for a in product((-1, 0, 1), repeat=d) if a != ((0,) * d)}