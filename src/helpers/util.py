from collections.abc import Iterable, Mapping, Sequence
from typing import Any, Callable, Optional, TypeVar

from itertools import islice, product, tee
import numpy as np
import re


_S = TypeVar('_S')
_T = TypeVar('_T')


def adj(coords: Sequence[Any, ...], diag=True) -> set[tuple[Any, ...]]:
    d = len(coords)
    return {tuple(a[i] + coords[i] for i in range(d))
            for a in product((-1, 0, 1), repeat=d)
            if (any(x != 0 for x in a) if diag else sum(x != 0 for x in a) == 1)}


def adj_np(coords: Sequence[Any, ...], diag=True) -> np.ndarray:
    d = len(coords)
    return np.array([[a[i] + coords[i] for i in range(d)]
                    for a in product((-1, 0, 1), repeat=d)
                    if (any(x != 0 for x in a) if diag else sum(x != 0 for x in a) == 1)])


def as_type(seq: Iterable[_S], type_conv: Callable[[_S], _T]) -> list[_T]:
    return [type_conv(x) for x in seq]


def as_grid(seq: Iterable[Iterable[_S]], type_conv: Optional[Callable[[_S], _T]] = None) -> list[list[_T]]:
    return [[type_conv(c) if type_conv else c for c in row] for row in seq]


def quict(dict_input: str, key: Callable[[str], _S] = str, val: Callable[[str], _T] = str) -> dict[_S, _T]:
    return dict((key(k), val(v)) for k, v in
                (re.split(r':\s?', pair) for pair in re.split(r',\s?', dict_input)))


def alph_ord(a: str, lower_off=0, upper_off=0) -> int:
    return alph_map(lower_off, upper_off)[a]


def alph_map(lower_off=0, upper_off=0) -> dict[str, int]:
    amap = {}
    for i in range(1, 27):
        amap[chr(i + 64)] = i + upper_off
        amap[chr(i + 96)] = i + lower_off
    return amap


def udlr(chars: Sequence[str] = 'UDLR'):
    """
    dict of (x, y) pairs corresponding to the first four characters in chars,
    corresponding to up, down, left, right, respectively
    """
    return dict(zip(chars, [(0, -1), (0, 1), (-1, 0), (1, 0)]))


def to_singleton_sets(sets: Mapping[_S, Iterable[_T]] | Sequence[Iterable[_T]],
                      raise_error=True) -> list[Optional[_T]] | dict[_S, Optional[_T]]:
    """Attempts to find a bijection which is a sub-mapping of the input one-to-many mapping"""

    # Copy the input into sets
    mapping: dict[_S, set[_T]]
    if isinstance(sets, Mapping):
        mapping = {k: set(v) for k, v in sets.items()}
    else:
        mapping = {i: set(v) for i, v in enumerate(sets)}
    while not all(len(v) <= 1 for _, v in mapping.items()):
        singletons = set()
        for _, v in mapping.items():
            if len(v) == 1:
                singletons.update(v)
        modified = False
        for _, v in mapping.items():
            orig_len = len(v)
            if orig_len > 1:
                v.difference_update(singletons)
                if len(v) != orig_len:
                    modified = True
        if not modified:
            if raise_error:
                raise ValueError('Could not find bijection: multiple options for some terms')
            else:
                for k, v in mapping.items():
                    if len(v) > 1:
                        mapping[k] = {next(iter(v))}
    if raise_error:
        for _, v in mapping.items():
            if len(v) < 1:
                raise ValueError('Could not find bijection: no possible option for some terms')
    if isinstance(sets, Mapping):
        return {k: next(iter(v), None) for k, v in mapping.items()}
    else:
        return [next(iter(mapping[i]), None) for i in range(len(sets))]


# https://stackoverflow.com/a/21303303
def nwise(iterable: Iterable[Any], n: int = 2):
    iterators = tee(iterable, n)
    for i, iterator in enumerate(iterators):
        next(islice(iterator, i, i), None)
    return zip(*iterators)


def shunt_yard(infix: str, op_map: Optional[Mapping[str, int]] = None) -> list[str]:
    """Dijkstra's Shunting Yard Algorithm for computing postfix notation from infix (useful in expression parsing)"""
    if op_map is None:
        op_map = {'+': 1, '-': 1, '*': 2, '/': 2}

    stack = []
    output = []
    for ch in infix:
        if len(ch.strip()) == 0:
            continue

        if ch == '(':
            stack.append(ch)
        elif ch == ')':
            while stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        elif ch in op_map:
            while len(stack) > 0 and stack[-1] != '(' and (stack[-1] not in op_map or op_map[stack[-1]] > op_map[ch]):
                output.append(stack.pop())
            stack.append(ch)
        else:
            output.append(ch)
    while len(stack) > 0:
        output.append(stack.pop())

    return output
