from typing import Any, Callable, Iterable, Optional, Sequence, TypeVar

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


# Dijkstra's Shunting Yard Algorithm for computing postfix notation from infix notation (useful in expression parsing)
def shunt_yard(infix: str, op_map: Optional[dict[str, int]] = None) -> list[str]:
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
