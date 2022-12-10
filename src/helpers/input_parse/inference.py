from __future__ import annotations

import json
from typing import Any, Optional
from typing import Generic, TypeVar
from abc import ABC, abstractmethod

from . import Input, StrInput

import ast
from .ast_util import ast_call_attr

from functools import reduce
from itertools import chain, combinations, product
from math import sqrt
import re

# class _InferAltern(NamedTuple, Generic[_T]):


class InputInference(ABC):
    _inp: StrInput
    _alternatives: list[tuple[ast.AST, float]]

    def __init__(self, inp: StrInput, input_var: str | ast.AST):
        self._inp = inp
        self._alternatives = self._process(input_var if isinstance(input_var, ast.AST) else ast.Name(input_var))

    @abstractmethod
    def _process(self, input_var: ast.AST) -> list[tuple[ast.AST, float]]:
        pass

    def get_expr(self, comment=False, max_alts=None) -> list[str]:
        def unparse(alt: tuple[ast.AST, Any]):
            if isinstance(alt[0], ast.expr):
                return ast.unparse(ast.Assign([ast.Name('p')], ast_call_attr(alt[0], 'native'), lineno=None))
            else:
                return ast.unparse(alt[0])

        return [re.sub(r'(^|\n)', r'\1# ' if comment and i > 0 else r'\1', unparse(a))
                for i, a in enumerate(sorted(
                        self._alternatives,
                        key=lambda t: t[1], reverse=True
                ))][:max_alts or len(self._alternatives)]

    def is_valid(self) -> bool:
        return len(self._alternatives) > 0


class JointInference(InputInference):
    def _process(self, input_var: ast.AST) -> list[tuple[ast.AST, float]]:
        rv = []

        for t in [
            StrInference,
            IntInference,
            JsonInference,
            StrListInference,
            IntListInference,
            TupleListInference,
            GridInference,
            SectionInference,
            IntsWithFluffInference,
            TableInference,
            AsmInference
        ]:
            rv.append(t(self._inp, input_var)._alternatives)

        return list(chain.from_iterable(rv))


class StrInference(InputInference):
    def _process(self, input_var: ast.AST) -> list[tuple[ast.AST, float]]:
        return [
            (input_var, 0.01)
        ]


class IntInference(InputInference):
    def _process(self, input_var: ast.AST) -> list[tuple[ast.AST, float]]:
        if re.fullmatch(r'^[+-]?\d+$', self._inp.native()):
            return [
                (ast_call_attr(input_var, 'int'), 0.1)
            ]
        else:
            return []


class JsonInference(InputInference):
    def _process(self, input_var: ast.AST) -> list[tuple[ast.AST, float]]:
        try:
            self._inp.json()
            return [
                (ast_call_attr(input_var, 'json'), 1.0 if '{' in self._inp.native() else 0.03)
            ]
        except json.JSONDecodeError:
            return []


class StrListInference(InputInference):
    def _process(self, input_var: ast.AST) -> list[tuple[ast.AST, float]]:
        native = self._inp.native()

        if '\n\n' in native:
            return [
                (ast_call_attr(input_var, 'split_paragraphs'), 0.4)
            ]
        elif '\n' in native:
            return [
                (ast_call_attr(input_var, 'splitlines'), 0.4)
            ]
        else:
            rv = []
            if ',' in native:
                rv.append((ast_call_attr(input_var, 'split', [ast.Constant(r',\s?')]),
                           0.35 if native.count(',') > 5 else 0.011))
            if '\t' in native:
                rv.append((ast_call_attr(input_var, 'split', [ast.Constant('\t')]),
                           0.35 if native.count(',') > 5 else 0.011))

            rv.append((ast_call_attr(input_var, 'list'), 0.005))

            return rv


class IntListInference(InputInference):
    def _process(self, input_var: ast.AST) -> list[tuple[ast.AST, float]]:
        native = self._inp.native()

        if '\n' in native and all(re.fullmatch(r'^[+-]?\d+$', s) for s in native.splitlines()):
            return [
                (ast_call_attr(ast_call_attr(input_var, 'splitlines'), 'int_list'), 0.7)
            ]
        elif ',' in native and all(re.fullmatch(r'^[+-]?\d+$', s) for s in re.split(r',\s?', native)):
            return [
                (ast_call_attr(ast_call_attr(input_var, 'split', [ast.Constant(r',\s?')]), 'int_list'), 0.65)
            ]
        elif all(re.fullmatch(r'^[+-]?\d+$', s) for s in re.split(r'\s', native)):
            return [
                (ast_call_attr(ast_call_attr(input_var, 'split', [ast.Constant(r'\s')]), 'int_list'), 0.65)
            ]
        elif re.fullmatch(r'^\d+$', native):
            return [
                (ast_call_attr(ast_call_attr(input_var, 'list'), 'int_list'), 0.06)
            ]
        else:
            return []


class TupleListInference(InputInference):
    def _process(self, input_var: ast.AST) -> list[tuple[ast.AST, float]]:
        # TODO
        return []


class GridInference(InputInference):
    def _process(self, input_var: ast.AST) -> list[tuple[ast.AST, float]]:
        native = self._inp.native()
        counts = sorted((native.count(c), c) for c in set(native).union({''}))

        rv = []
        for outer, inner in combinations(counts, r=2):
            # print(outer, inner, inner[0] % (outer[0] + 1))
            if inner[0] <= 1 or inner[0] % (outer[0] + 1) != 0:
                continue
            split = native.split(outer[1])
            if len(split) <= 2:
                continue
            per_ln = split[0].count(inner[1])
            if per_ln <= (2 if inner[1] == '' else 1) or not all(t.count(inner[1]) == per_ln for t in split[1:]):
                continue

            if inner[1].isalnum() or outer[1].isalnum():
                score = 0.018
            elif outer[1] == '\n':
                score = 0.72
            else:
                score = 0.14

            splits: list[Any] = [ast.Constant(None if x == '' else x) for x in (outer[1], inner[1])]
            rv.append((ast_call_attr(ast_call_attr(
                ast_call_attr(input_var, 'grid', [ast.List(splits)]),
                'opt_int'), 'np'), score))
        return rv


class SectionInference(InputInference):
    def _process(self, input_var: ast.AST) -> list[tuple[ast.AST, float]]:
        native = self._inp.native()
        count = native.count('\n\n')
        if count < 1 or count > 4:
            return []
        assignment = ast.Assign([ast.Tuple([ast.Name(f'sec{d}') for d in range(count + 1)])],
                                ast_call_attr(input_var, 'split_paragraphs'), lineno=None)

        sections = [JointInference(inp, f'sec{ix}')._alternatives for ix, inp in enumerate(self._inp.split_paragraphs())]
        rv = []
        for c in product(*sections):
            statements = [assignment, *(ast.Assign([ast.Name(f'p{i}')], ast_call_attr(a[0], 'native'), lineno=None)
                                        for i, a in enumerate(c))]
            rv.append((ast.Module(statements, type_ignores=[]), sqrt(reduce(lambda part, alt: part * alt[1], c, 1))))

        return rv

    def get_expr(self, comment=False, max_alts=None) -> list[str]:
        return [('# ' if comment and i > 0 else '') + ast.unparse(a[0])
                for i, a in enumerate(sorted(
                        self._alternatives,
                        key=lambda t: t[1], reverse=True
                ))][:max_alts or len(self._alternatives)]


class IntsWithFluffInference(InputInference):
    def _process(self, input_var: ast.AST) -> list[tuple[ast.AST, float]]:
        if re.match(r'[\s\S]*\d+[\s\S]*', self._inp.native()) and not re.fullmatch(r'[+-]?\d+', self._inp.native()):
            return [
                (ast_call_attr(ast_call_attr(input_var, 'extract', [ast.Constant(r'[+-]?\d+')]), 'int_list'),
                 0.02 if len(self._inp) < 100 else 0.0001)
            ]
        else:
            return []


class TableInference(InputInference):
    def _process(self, input_var: ast.AST) -> list[tuple[ast.AST, float]]:
        # TODO
        return []


class AsmInference(InputInference):
    def _process(self, input_var: ast.AST) -> list[tuple[ast.AST, float]]:
        # TODO
        return []