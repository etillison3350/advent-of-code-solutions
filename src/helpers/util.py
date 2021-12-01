from typing import Any, Callable, Iterable, Sequence, TypeVar

from itertools import islice, product, tee


T = TypeVar('T')


def adj(co):
    d = len(co)
    return {tuple(a[i] + co[i] for i in range(d)) for a in product((-1, 0, 1), repeat=d) if a != ((0,) * d)}


def as_type(seq: Sequence[str], type_conv: Callable[[str], T]) -> list[T]:
    return [type_conv(x) for x in seq]


# https://stackoverflow.com/a/21303303
def nwise(iterable: Iterable[Any], n: int = 2):
    iterators = tee(iterable, n)
    for i, iterator in enumerate(iterators):
        next(islice(iterator, i, i), None)
    return zip(*iterators)