from typing import Callable, Generator, Iterable, NamedTuple, Optional, Sequence, TypeVar, Generic, Any
from enum import Enum

import os

from collections import defaultdict
import math
import re


T = TypeVar('T')

_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


class _LazyDict(defaultdict):
    default_factory: Optional[Callable[[_KT], _VT]]

    def __missing__(self, key):
        value = self.default_factory(key)
        self[key] = value
        return value


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
    syms: set


_IRegex = Sequence[_IReTerm]


class LevOp(Enum):
    """An valid operation on a string, for computing Levenshtein distance"""
    MATCH = 0,   # Characters match (no-op)
    NEW = 1,     # Add a character
    MODIFY = 2,  # Change a character
    DELETE = 3,  # Remove a character

    SWAP = 4,  # Swap two characters (Damerau-Levenshtein distance)

    # Regex-specific operations
    IGNORE_OPTIONAL = 5,   # Ignore an optional term (no-op)
    MODIFY_ADD_CLASS = 6,  # Change a group by adding an element of a different character class (special case of MODIFY)
    SWAP_MERGE_CLASS = 7   # Merge consecutive groups of different character classes (special case of SWAP)


def _get_default_costs() -> dict[LevOp, int]:
    """Get the default costs of the operations used in calculating Levenshtein distance"""
    return {
        None: math.inf,
        LevOp.NEW: 12,
        LevOp.MODIFY: 10,
        LevOp.MODIFY_ADD_CLASS: 15,
        LevOp.DELETE: 11,
        LevOp.SWAP: 14,
        LevOp.SWAP_MERGE_CLASS: 29,
        LevOp.MATCH: 2,
        LevOp.IGNORE_OPTIONAL: 3
    }


def _get_default_char_classes() -> list[set]:
    """Get the default set of character classes that the regex generator should attempt to find: [a-z], [A-Z], \\d"""
    return [
        set(chr(x) for x in range(ord('A'), ord('Z') + 1)),
        set(chr(x) for x in range(ord('a'), ord('z') + 1)),
        set(chr(x) for x in range(ord('0'), ord('9') + 1))
    ]


# ---------- Regular Expression Generation ---------- #


def _generate_regex(strings: Iterable[Sequence],
                    tree=False,
                    classes: Optional[Sequence[set]] = None,
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

    string_iter = iter(strings)
    regex_list: list[_IRegex] = [[_IReTerm(_IReQuant(1, 1), {token}) for token in next(string_iter)]]

    for input_string in string_iter:
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
                     input_string: Sequence,
                     classes: Sequence[set],
                     costs: dict[LevOp, int]) -> list[list[tuple[int, list[LevOp]]]]:
    """Evaluate the Levenshtein distance between a regex and a string, using dynamic programming, and return the
    dynamic programming table"""

    # Create table, populate base cases
    table = [[(costs[LevOp.NEW] * x, [LevOp.NEW]) for x in range(len(input_string) + 1)] for _ in range(len(regex) + 1)]
    table[0][0] = (0, [])
    for y, term in enumerate(regex):
        op = LevOp.DELETE if term.quant.lo > 0 else LevOp.IGNORE_OPTIONAL
        table[y + 1][0] = (table[y][0][0] + costs[op], [op])

    # Additional memoization information
    match_table = [[char in term.syms for char in input_string] for term in regex]
    cls_list: dict[int, set[int]] = \
        _LazyDict(lambda ix: set(i for i, cls in enumerate(classes) if len(cls.intersection(regex[ix].syms)) > 0))

    # Compute remaining table values
    for y, term in enumerate(regex):
        for x, char in enumerate(input_string):
            if match_table[y][x]:
                mod_op = LevOp.MATCH
            elif len(classes) == 0 or any(char in classes[cls_index] for cls_index in cls_list[y]):
                mod_op = LevOp.MODIFY
            else:
                mod_op = LevOp.MODIFY_ADD_CLASS

            if term.quant.lo > 0:
                rmv_op = LevOp.DELETE
            else:
                rmv_op = LevOp.IGNORE_OPTIONAL

            new_op = LevOp.NEW

            if x > 0 and y > 0 and match_table[y - 1][x] and match_table[y][x - 1]:
                if len(classes) > 0 and cls_list[y].isdisjoint(cls_list[y - 1]):
                    swp_op = LevOp.SWAP_MERGE_CLASS
                else:
                    swp_op = LevOp.SWAP
            else:
                swp_op = None

            mod = table[y][x][0] + costs[mod_op]
            rmv = table[y][x + 1][0] + costs[rmv_op]
            new = table[y + 1][x][0] + costs[new_op]
            swp = table[y - 1][x - 1][0] + costs[swp_op]

            min_cost = min(mod, rmv, new, swp)

            src = list(sorted(
                (op for op, cost in zip((mod_op, rmv_op, new_op, swp_op), (mod, rmv, new, swp)) if cost == min_cost),
                key=lambda o: costs[o]
            ))

            table[y + 1][x + 1] = (min_cost, src)
    return table


def _print_table(table: list[list[tuple[int, list[LevOp]]]], regex: _IRegex, input_str: Sequence):
    print(' ' * 33, end='')
    for char in input_str:
        print("{:<6}".format(char), end=' ')
    print()
    for index, row in enumerate(table):
        if index == 0:
            print(' ' * 25, end=' ')
        else:
            print('{:>25}'.format(_iregex_as_string([regex[index - 1]])[:20]), end=' ')
        for col, src in row:
            print("{:<3}{:<3}".format(col, ''.join(str(s.name[0]) for s in src)), end=' ')
        print()


def _create_new_regex(table: list[list[tuple[int, list[LevOp]]]],
                      regex: _IRegex,
                      input_string: Sequence,
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
            new_term = _IReTerm(_IReQuant(0, 1), {input_string[x - 1]})
            for rx in _create_new_regex(table, regex, input_string, (x - 1, y), return_multiple, memo):
                new_regex_list.append([*rx, new_term])
        elif op == LevOp.MODIFY or op == LevOp.MODIFY_ADD_CLASS:
            new_syms = {input_string[x - 1]}
            new_syms.update(regex[y - 1].syms)
            new_term = _IReTerm(regex[y - 1].quant, new_syms)
            for rx in _create_new_regex(table, regex, input_string, (x - 1, y - 1), return_multiple, memo):
                new_regex_list.append([*rx, new_term])
        elif op == LevOp.DELETE:
            new_term = _IReTerm(_IReQuant(0, 1), regex[y - 1].syms)
            for rx in _create_new_regex(table, regex, input_string, (x, y - 1), return_multiple, memo):
                new_regex_list.append([*rx, new_term])
        elif op == LevOp.SWAP:
            new_syms = regex[y - 1].syms.union(regex[y - 2].syms)
            new_quant = sorted((regex[y - 1].quant, regex[y - 2].quant))
            new_terms = _IReTerm(new_quant[0], new_syms), _IReTerm(new_quant[0], new_syms)
            for rx in _create_new_regex(table, regex, input_string, (x - 2, y - 2), return_multiple, memo):
                new_regex_list.append([*rx, *new_terms])
        elif op == LevOp.MATCH:
            for rx in _create_new_regex(table, regex, input_string, (x - 1, y - 1), return_multiple, memo):
                new_regex_list.append([*rx, regex[y - 1]])
        elif op == LevOp.IGNORE_OPTIONAL:
            for rx in _create_new_regex(table, regex, input_string, (x, y - 1), return_multiple, memo):
                new_regex_list.append([*rx, regex[y - 1]])

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


# ---------- Pre- and Post-Processing Strategies ---------- #


def _transform_multiple(regex: _IRegex,
                        *transformations: Callable[[_IRegex], _IRegex],
                        maxiter: Optional[int] = 10):
    original_length = len(regex)

    iteration = 0
    while maxiter is None or iteration < maxiter:
        iteration += 1

        for trans in transformations:
            regex = trans(regex)

        if len(regex) == original_length:
            break
        original_length = len(regex)

    return regex


def _convert_class_to_index(input_list: Iterable[Sequence[T]],
                            classes: Optional[Sequence[set[T]]] = None) -> list[tuple[T | int]]:
    if classes is None:
        classes = _get_default_char_classes()

    new_inputs = []
    for input_string in input_list:
        new_string = []
        for ch in input_string:
            cls_mask = 0
            for ix, cls in enumerate(classes):
                if ch in cls:
                    cls_mask |= (1 << ix)
            new_string.append(cls_mask or ch)
        new_inputs.append(tuple(new_string))
    return new_inputs


def _transform_index_to_class(regex: _IRegex, classes: Optional[Sequence[set[T]]] = None) -> _IRegex:
    if classes is None:
        classes = _get_default_char_classes()

    new_regex = []
    for term in regex:
        syms = set()
        for cls in term.syms:
            if type(cls) == int and cls > 0:
                syms.update(classes[int.bit_length(cls) - 1])
            else:
                syms.add(cls)
        new_regex.append(_IReTerm(term.quant, syms))
    return new_regex


def _convert_split(input_list: Iterable[str], split: str = '(?<=\\W)|(?=\\W)') -> list[list[str]]:
    return [re.split(split, input_string) for input_string in input_list]


def _transform_generalize_to_classes(regex: _IRegex,
                                     classes: Optional[Sequence[set]] = None,
                                     similarity: float | int = 0.2) -> _IRegex:
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


def _transform_merge_quantifiers(regex: _IRegex,
                                 reverse=False,
                                 classes=None,
                                 method: str = 'subset', recursive=True) -> _IRegex:
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
        return _transform_merge_quantifiers(new_regex, not reverse, classes, method, recursive)


# ---------- String Conversion ---------- #


def _get_named_character_classes() -> dict[str, set[str]]:
    return {
        '\\w': set(x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'),
        '\\d': set(chr(x) for x in range(ord('0'), ord('9') + 1)),
        '\\s': set(x for x in ' \f\n\r\t')
    }


def _iregex_as_string(regex: _IRegex, quant_limit: int = 0, esc=True, capture: str = 'none'):
    esc_chars = None if esc else []
    out = ''
    capture_group = ''
    for term in regex:
        syms = {str(token) for token in term.syms}
        quant = term.quant
        if '' in syms:  # (<empty>|str1|...)+ is equivalent to (str1|...)*
            syms.remove('')
            quant = _IReQuant(0, quant.hi)
        if len(syms) == 0:  # If there are no possible options, just ignore this term
            continue

        # Alternation
        if len(syms) == 1:  # One possible token
            token = next(iter(syms))
            if len(token) > 1 and quant != (1, 1):  # If token is multiple chars, wrap in non-capturing group
                group_str = '(?:' + _escape(token, esc_chars) + ')'
            else:  # Otherwise, it can be included as-is
                group_str = _escape(token, esc_chars)
        elif all(len(token) == 1 for token in syms):  # Many possible terms, all single characters (use [] notation)
            group_str = ''
            num_names = 0
            # Apply named character classes: \d, \s, etc.
            for name, char_cls in _get_named_character_classes().items():
                if syms.issuperset(char_cls):
                    group_str += name
                    syms = syms.difference(char_cls)
                    num_names += 1
            if len(syms) == 0:  # If all of the tokens can be represented by named classes, we're done
                if num_names != 1:  # We don't even need brackets if it's just one class
                    group_str = '[' + group_str + ']'
            else:  # Otherwise, list the (additional) characters in brackets
                group_str = '[' + group_str
                token_iter = iter(sorted(syms))
                range_bounds = [ord(next(token_iter))] * 2
                for token in token_iter:  # Find consecutive characters, and represent them as ranges (e.g. [a-g])
                    if ord(token) == range_bounds[1] + 1:
                        range_bounds[1] += 1
                    else:
                        group_str += _escape_range(*range_bounds)
                        range_bounds = [ord(token)] * 2
                group_str += _escape_range(*range_bounds) + ']'
        else:  # Many possible token, not all single characters: use alternation (?:token_1|token_2|...)
            group_str = '(?:' + '|'.join(_escape(token, esc_chars) for token in sorted(syms)) + ')'

        # Quantifiers
        if quant == (0, 1):
            group_str += '?'
        elif quant == (1, 1):
            pass
        elif quant.hi > quant_limit and quant.lo == 0:
            group_str += '*'
        elif quant.hi > quant_limit and quant.hi - quant.lo > quant_limit:
            group_str += '+'
        elif quant.lo == quant.hi:
            if len(group_str) == 1 and quant.lo < 6:
                group_str *= quant.lo
            else:
                group_str += '{{{}}}'.format(quant.lo)
        else:
            group_str += '{{{},{}}}'.format(*quant)

        if capture == 'consecutive':
            if quant.lo == quant.hi and len(term.syms) == 1:
                if len(capture_group) > 0:
                    out += '(' + capture_group + ')'
                capture_group = ''
                out += group_str
            else:
                capture_group += group_str
        elif capture == 'each' and (quant.lo != quant.hi or len(term.syms) != 1):
            out += '(' + group_str + ')'
        else:
            out += group_str

    if len(capture_group) > 0:
        if len(out) == 0:
            out = capture_group
        else:
            out += '(' + capture_group + ')'

    return out


def _escape_range(lower_ord: int, upper_ord: int) -> str:
    if upper_ord - lower_ord > 2:
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

                        if len(inp) < 3:
                            continue
                        print()
                        print(file, inp[0])

                        *_, re_list = _generate_regex(_convert_class_to_index(str) for str in _convert_split(inp))
                        for regex in re_list:
                            print(regex)
                            regex_str = _iregex_as_string(_transform_merge_quantifiers(regex),
                                                          capture='consecutive',
                                                          quant_limit=0)
                            print(regex_str)

                            # if len(regex_str) < 511:
                            #     for s in inp[:8]:
                            #         match = re.fullmatch(regex_str, s)
                            #
                            #         if match is None:
                            #             print(s)
                            #             assert match is not None
                            #         elif len(match.groups()) > 0:
                            #             print(s)
                            #             print(match.groups())

                        # *_, re_list = _generate_regex(inp)
                        # for regex in re_list:
                        #     regex_str = _iregex_as_string(_transform_multiple(regex, _transform_generalize_to_classes, _transform_merge_quantifiers), capture='consecutive',
                        #                                   quant_limit=0)
                        #     print(regex_str)
                        #
                        #     if len(regex_str) < 511:
                        #         for s in inp[:8]:
                        #             match = re.fullmatch(regex_str, s)
                        #
                        #             if match is None:
                        #                 print(s)
                        #                 assert match is not None
                        #             elif len(match.groups()) > 0:
                        #                 print(s)
                        #                 print(match.groups())
                        #
                        # classes = _get_default_char_classes()
                        # inp_cls = _convert_class_to_index(inp, classes)
                        #
                        # # *_, re_list = _generate_regex(inp, tree=False)
                        # # for regex in re_list:
                        # #     print(_apply_quantifiers(regex))
                        # #     print(_iregex_as_string(regex))
                        #
                        # *_, re_list = _generate_regex(inp_cls, classes=[set()])
                        # for rx in re_list:
                        #     regex = _transform_index_to_class(rx, classes)
                        #
                        #     print(_iregex_as_string(regex))
                        #     regex_str = _iregex_as_string(_transform_merge_quantifiers(regex), capture='consecutive', quant_limit=0)
                        #     print(regex_str)
                        #
                        #     if len(regex_str) < 511:
                        #         for s in inp[:8]:
                        #             match = re.fullmatch(regex_str, s)
                        #
                        #             if match is None:
                        #                 print(s)
                        #                 assert match is not None
                        #             elif len(match.groups()) > 0:
                        #                 print(s)
                        #                 print(match.groups())
