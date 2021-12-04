from typing import Generator, Iterable, NamedTuple, Optional, Sequence
from enum import Enum

from collections import defaultdict
import math


class _IReQuant(NamedTuple):
    """A regex quantifier, consisting of a lower and upper bound"""
    lo: int
    hi: int

    def __add__(self, other):
        lo = self.lo + other.lo
        hi = self.hi + other.hi
        return _IReQuant(lo, hi)


class _IReTerm(NamedTuple):
    """A term in a regular expression, consisting of a set `syms` of valid tokens (usually characters) and a range
    `quant` of times these tokens can be repeated"""
    quant: _IReQuant
    syms: set[any]


_IRegex = list[_IReTerm]


class LevOp(Enum):
    """An valid operation on a string, for computing Levenshtein distance"""
    MATCH = 0,   # Characters match (no-op)
    NEW = 1,     # Add a character
    MODIFY = 2,  # Change a character
    DELETE = 3,  # Remove a character

    # Regex-specific operations
    IGNORE_OPTIONAL = 4,  # Ignore an optional term (no-op)
    MODIFY_ADD_CLASS = 5  # Change a group by adding an element of a different character class (special case of MODIFY)


def _get_default_costs() -> dict[LevOp, int]:
    """Get the default costs of the operations used in calculating Levenshtein distance"""
    return {
        LevOp.NEW: 12,
        LevOp.MODIFY: 10,
        LevOp.DELETE: 11,
        LevOp.MODIFY_ADD_CLASS: 15,
        LevOp.MATCH: 2,
        LevOp.IGNORE_OPTIONAL: 3
    }


CharClassList = list[set[str]]


def _get_default_char_classes() -> CharClassList:
    """Get the default set of character classes that the regex generator should attempt to find: [a-z], [A-Z], \\d,
    and \\s """
    return [
        set(chr(x) for x in range(ord('A'), ord('Z') + 1)),
        set(chr(x) for x in range(ord('a'), ord('z') + 1)),
        set(chr(x) for x in range(ord('0'), ord('9') + 1)),
        set(' \f\n\r\t\v')
    ]


# ---------- Regular Expression Generation ---------- #


def _generate_regex(strings: Iterable[Sequence[str]],
                    tree: False,
                    classes: Optional[CharClassList] = None,
                    costs: Optional[dict[LevOp, int]] = None) -> Generator[list[_IRegex], None, None]:
    """Generate a simple regular expression."""

    if next(iter(strings), None) is None:
        return

    if costs is None:
        costs = _get_default_costs()
    else:
        for k, v in _get_default_costs().items():
            if k not in costs:
                costs[k] = v

    if classes is None:
        classes = _get_default_char_classes()

    regex_list: list[_IRegex] = [[_IReTerm(_IReQuant(1, 1), {token}) for token in next(iter(strings))]]

    for input_string in strings[1:]:
        try:
            new_regex_list = []
            min_cost = math.inf
            for regex in regex_list:
                table = _construct_table(regex, input_string, classes, costs)

                # Only consider the regexes with the minimum cost to modify
                if table[-1][-1][0] < min_cost:
                    min_cost = table[-1][-1][0]
                    new_regex_list = []

                created_regex = _create_new_regex(table, regex, input_string, (len(table[0]) - 1, len(table) - 1), tree)
                new_regex_list.extend(created_regex)
        except RecursionError:  # For large tables, _create_new_regex may exceed the maximum recursion depth
            break

        patterns = _get_patterns(new_regex_list)
        regex_list = _coalesce_patterns(patterns)

        yield regex_list


def _construct_table(regex: _IRegex,
                     input_string: Sequence[str],
                     classes: CharClassList,
                     costs: dict[LevOp, int]) -> list[list[tuple[int, list[LevOp]]]]:
    """Evaluate the Levenshtein distance between a regex and a string, using dynamic programming, and return the
    dynamic programming table"""

    table = [[(costs[LevOp.NEW] * x, [LevOp.NEW]) for x in range(len(input_string) + 1)] for _ in range(len(regex) + 1)]
    table[0][0] = (0, [])
    for y, term in enumerate(regex):
        op = LevOp.IGNORE_OPTIONAL if term.quant.lo > 0 else LevOp.DELETE
        table[y + 1][0] = (table[y][0][0] + costs[op], [op])
    for y, term in enumerate(regex):
        for x, char in enumerate(input_string):
            if char in term.syms:
                modify_op = LevOp.MATCH
            elif len(classes) == 0 or any(char in cls for cls in classes if len(cls.intersection(term.syms)) > 0):
                modify_op = LevOp.MODIFY
            else:
                modify_op = LevOp.MODIFY_ADD_CLASS

            if term.quant.lo > 0:
                remove_op = LevOp.DELETE
            else:
                remove_op = LevOp.IGNORE_OPTIONAL

            new_op = LevOp.NEW

            mod = table[y][x][0] + costs[modify_op]
            rmv = table[y][x + 1][0] + costs[remove_op]
            new = table[y + 1][x][0] + costs[new_op]

            min_cost = min(mod, rmv, new)

            src = list(sorted(
                (op for op, cost in zip((modify_op, remove_op, new_op), (mod, rmv, new)) if cost == min_cost),
                key=lambda o: costs[o]
            ))

            table[y + 1][x + 1] = (min_cost, src)
    return table


def _create_new_regex(table: list[list[tuple[int, list[LevOp]]]],
                      regex: _IRegex,
                      input_string: Sequence[str],
                      pos: tuple[int, int],
                      return_multiple=False,
                      memo: Optional[dict[tuple[int, int], list[_IRegex]]] = None) -> list[_IRegex]:
    """Recursively traverse through the table to modify the given regex to accommodate the input string"""

    if memo is None:
        memo = {}
    elif pos in memo:
        return memo[pos]

    x, y = pos
    _, ops = table[y][x]

    if len(ops) == 0:
        return [[]]

    new_regex_list: list[_IRegex] = []
    for op in ops:
        if op == LevOp.NEW:
            for re in _create_new_regex(table, regex, input_string, (x - 1, y), return_multiple, memo):
                new_regex_list.append(re + [_IReTerm(_IReQuant(0, 1), {input_string[x - 1]})])
        elif op == LevOp.MODIFY or op == LevOp.MODIFY_ADD_CLASS:
            for re in _create_new_regex(table, regex, input_string, (x - 1, y - 1), return_multiple, memo):
                new_syms = {input_string[x - 1]}
                new_syms.update(regex[y - 1].syms)
                new_regex_list.append(re + [_IReTerm(regex[y - 1].quant, new_syms)])
        elif op == LevOp.DELETE:
            for re in _create_new_regex(table, regex, input_string, (x, y - 1), return_multiple, memo):
                new_regex_list.append(re + [_IReTerm(_IReQuant(0, 1), regex[y - 1].syms)])
        elif op == LevOp.MATCH:
            for re in _create_new_regex(table, regex, input_string, (x - 1, y - 1), return_multiple, memo):
                new_regex_list.append(re + [regex[y - 1]])
        elif op == LevOp.IGNORE_OPTIONAL:
            for re in _create_new_regex(table, regex, input_string, (x, y - 1), return_multiple, memo):
                new_regex_list.append(re + [regex[y - 1]])
        if not return_multiple:
            break

    if len(new_regex_list) > 1:
        patterns = _get_patterns(new_regex_list)
        memo[pos] = _coalesce_patterns(patterns)
    else:
        memo[pos] = new_regex_list

    return memo[pos]


def _get_patterns(regex_list: list[_IRegex]) -> dict[tuple, list[_IRegex]]:
    patterns: defaultdict[tuple, list[_IRegex]] = defaultdict(list)
    for regex in regex_list:
        patterns[tuple(term.quant.lo > 0 for term in regex)].append(regex)
    return patterns


def _coalesce_patterns(patterns: dict[tuple, list[_IRegex]]) -> list[_IRegex]:
    min_len = min(len(pat) for pat in patterns.keys())
    regex_list = []
    for pattern, regexes in patterns.items():
        if len(pattern) > min_len:
            continue

        if len(regexes) == 1:
            regex_list.append(regexes[0])
        else:
            new_regex: _IRegex = [_IReTerm(_IReQuant(opt, 1), set()) for opt in pattern]
            for regex in regexes:
                for i, term in enumerate(regex):
                    new_regex[i].syms.update(term.syms)
            regex_list.append(new_regex)
    return regex_list


# ---------- Regular Expression Transformation ---------- #


def _apply_all_transformations(regex: _IRegex, maxiter: Optional[int] = 10):
    original_length = len(regex)

    iteration = 0
    while maxiter is None or iteration < maxiter:
        iteration += 1

        regex = _apply_classes(regex)
        regex = _apply_quantifiers(regex, method='subset')
        regex = _apply_quantifiers(regex, method='class')

        if len(regex) == original_length:
            break
        original_length = len(regex)

    return regex


def _apply_classes(regex: _IRegex, classes=None, similarity: float | int = 0.2) -> _IRegex:
    if classes is None:
        classes = _get_default_char_classes()

    new_regex = []
    for term in regex:
        new_syms = set(term.syms)
        for cls in classes:
            if len(cls.intersection(term.syms)) > (similarity * len(cls) if similarity < 1 else similarity):
                new_syms.update(cls)
        new_regex.append(_IReTerm(term.quant, new_syms))
    return new_regex


def _apply_quantifiers(regex: _IRegex, reverse=False, classes=None, method: str = 'subset', recursive=True) -> _IRegex:
    if len(regex) <= 1:
        return regex

    if method == 'class' and classes is None:
        classes = _get_default_char_classes()

    new_regex = []

    term_iter = reversed(regex) if reverse else iter(regex)
    curr: Optional[_IReTerm] = None
    if method == 'class':
        for term in term_iter:
            cls = None
            if curr is not None and curr.quant != (1, 1) and term.quant != (1, 1):
                cls = next((c for c in classes if c.issuperset(curr[1]) and c.issuperset(term.syms)), None)

            if cls is None:
                if curr is not None:
                    new_regex.append(curr)
                curr = term
            else:
                curr = _IReTerm(curr.quant + term.quant, cls)
    else:
        for term in term_iter:
            if curr is None or not (curr[1].issuperset(term.syms) or curr[1].issubset(term.syms)):
                if curr is not None:
                    new_regex.append(curr)
                curr = term
            else:
                curr = _IReTerm(curr.quant + term.quant, curr.syms.union(term.syms))

    new_regex.append(curr)

    if reverse:
        new_regex.reverse()

    if not recursive or len(regex) == len(new_regex):
        return new_regex
    else:
        return _apply_quantifiers(new_regex, not reverse, classes, method, recursive)


# ---------- String Conversion ---------- #


def _iregex_as_string(re: _IRegex, esc=True):
    esc_chars = None if esc else []
    out = ''
    for term in re:
        if len(term.syms) == 1:
            token = next(iter(term.syms))
            if len(token) > 1 and term.quant != (1, 1):
                group_str = '(?:' + _escape(token, esc_chars) + ')'
            else:
                group_str = _escape(token, esc_chars)
        elif all(len(token) == 1 for token in term.syms):
            group_str = '['
            token_iter = iter(sorted(term.syms))
            group = [ord(next(token_iter))] * 2
            for token in token_iter:
                if ord(token) == group[1] + 1:
                    group[1] += 1
                else:
                    group_str += _group_as_range(*group)
                    group = [ord(token)] * 2
            group_str += _group_as_range(*group)
            group_str += ']'

            if group_str == '[0-9]':
                group_str = '\\d'
        else:
            group_str = '(?:' + '|'.join(_escape(sym, esc_chars) for sym in sorted(term.syms)) + ')'

        if term.quant == (0, 1):
            group_str += '?'
        elif term.quant == (1, 1):
            pass
        elif term.quant[1] > 5 and term.quant[0] == 0:
            group_str += '*'
        elif term.quant[1] > 5 and term.quant[0] < term.quant[1] / 2:
            group_str += '+'
        elif term.quant[0] == term.quant[1]:
            if len(group_str) == 1 and term.quant[0] < 6:
                group_str *= term.quant[0]
            else:
                group_str += '{{{}}}'.format(term.quant[0])
        else:
            group_str += '{{{},{}}}'.format(*term.quant)
        out += group_str
    return out


def _group_as_range(lower_ord: int, upper_ord: int) -> str:
    if upper_ord - lower_ord > 1:
        return _escape(lower_ord) + '-' + _escape(upper_ord)
    else:
        return ''.join(_escape(c) for c in range(lower_ord, upper_ord + 1))


def _escape(string: str | int, chars: Optional[Sequence[str]] = None) -> str:
    if type(string) == int:
        string = chr(string)
    elif len(string) != 1:
        return ''.join(_escape(c, chars) for c in string)

    if string in ('.*+?^${}()|[-]\\' if chars is None else chars):
        return '\\' + string
    else:
        return string


import re, os


if __name__ == '__main__':
    dir = '..\\inputs'
    for dirpath, dirnames, filenames in os.walk(dir):
        for file in filenames:
            if file.startswith('input'):
                with open(os.path.join(dirpath, file), 'r') as inp_file:
                    whole_inp = inp_file.read()
                    parts = whole_inp.split('\n\n')
                    if len(parts) > 4:
                        parts = ['\n'.join(part.replace('\n', '$') for part in parts)]
                    for part_inp in parts:
                        inp = part_inp.splitlines()[1:]

                        if len(inp) == 0:
                            continue
                        print()
                        print(file, inp[0])

                        *_, re_list = _generate_regex(inp, tree=False)
                        for regex in re_list:
                            print(_iregex_as_string(regex))
                            regex_str = _iregex_as_string(_apply_all_transformations(regex))
                            print(regex_str)
                            if len(regex_str) < 255 and not all(re.fullmatch(regex_str, s) is not None for s in inp[:16]):
                                print([s for s in inp[:16] if re.fullmatch(regex_str, s) is None])
                                assert False
