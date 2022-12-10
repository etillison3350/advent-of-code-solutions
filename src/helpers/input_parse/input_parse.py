from __future__ import annotations

from typing import Any, Callable, Generator, Iterable, Mapping, Optional, Sequence
from typing import Generic, TypeVar
from numpy.typing import ArrayLike

from abc import ABC, abstractmethod

from itertools import chain, pairwise
import json
import re

import pandas as pd
import numpy as np


# -------- BASIC INPUTS -------- #

_T = TypeVar('_T')
_V = TypeVar('_V')


class Input(ABC, Generic[_T, _V]):
    _inp: _V

    def __init__(self, inp: _V):
        self._inp = inp

    @abstractmethod
    def native(self) -> _T:
        pass

    def str(self) -> StrInput:
        return StrInput(str(self._inp))

    def __str__(self) -> str:
        return self.str().native_str()

    def int(self) -> IntInput:
        return IntInput(int(self._inp))

    def __int__(self):
        return self.int().native_int()


class BasicInput(Generic[_T], Input[_T, _T]):
    _inp: _T

    def __init__(self, inp: _T):
        super().__init__(inp)

    def native(self) -> _T:
        return self._inp


class StrInput(BasicInput[str]):
    _inp: str

    def __init__(self, inp: str):
        super().__init__(inp)

    def native_str(self):
        return self._inp

    def list(self):
        return StrListInput(self._inp)

    def split(self,
              split_seq: Optional[str] = r'\s',
              max_split: int = 0,
              flags: int | re.RegexFlag = 0,
              remove_empty=False) -> StrListInput:
        if split_seq is None:
            return self.list()
        else:
            return StrListInput(s for s in re.split(split_seq, self._inp, max_split, flags) if s or not remove_empty)

    def splitlines(self) -> StrListInput:
        return self.split('\n')

    def split_paragraphs(self) -> StrListInput:
        return self.split('\n\n')

    def strip(self) -> StrInput:
        return StrInput(self._inp.strip())

    def sections(self,
                 *classes: str,
                 include_no_match=True,
                 remove_empty=True,
                 opt_int=True) -> StrListInput | ListInput[str | int]:
        if len(classes) == 0:
            classes = ['A-Za-z', '0-9']
        return self.extract(*[f'[{c}]+' for c in classes],
                            include_no_match=include_no_match,
                            remove_empty=remove_empty,
                            opt_int=opt_int)

    def extract(self,
                *patterns: str,
                include_no_match=True,
                remove_empty=True,
                opt_int=False) -> StrListInput | ListInput[str | int]:
        pat = '|'.join(f'(?:{p})' for p in patterns)

        segments = chain([(0, 0)], (m.span() for m in re.finditer(pat, self._inp)), [(len(self._inp), len(self._inp))])
        if include_no_match:
            segments = chain.from_iterable((lo, (lo[1], hi[0])) for lo, hi in pairwise(segments))
        sections = StrListInput(self._inp[lo:hi] for lo, hi in segments if not remove_empty or lo != hi)
        if opt_int:
            return MixedListInput(sections.opt_int())
        else:
            return sections

    _C = TypeVar('_C')

    def grid(self,
             splits: Optional[Sequence[str]] = None,
             cvt: Optional[Callable[[str], _C] | Mapping[str, _C]] = None) -> ListInput:
        if splits is None:
            splits = ['\n', None]
        rv: StrInput | ListInput = self
        for s in splits:
            rv = rv.split(s)
        if cvt is not None:
            rv = rv.map(cvt)
        return rv

    def grid_int(self, splits: Optional[Sequence[str]] = None):
        return self.grid_np(splits, int)

    def grid_np(self,
                splits: Optional[Sequence[str]] = None,
                cvt: Optional[Callable[[str], _C] | Mapping[str, _C]] = None) -> NumpyInput:
        return self.grid(splits, cvt).np()

    def opt_int(self) -> StrInput | IntInput:
        if re.fullmatch(r'^[+-]?\d+$', self._inp):
            return self.int()
        else:
            return self

    def json(self):
        return BasicInput(json.loads(self._inp))

    def __iter__(self) -> Generator[str, None, None]:
        yield from self._inp

    def __getitem__(self, index):
        return StrInput(self._inp[index])

    def __len__(self):
        return len(self._inp)


class IntInput(BasicInput[int]):
    _inp: int

    def __init__(self, inp: int):
        super().__init__(inp)

    def native_int(self):
        return self._inp


# -------- LIST INPUTS -------- #

_E = TypeVar('_E')


class ListInput(Generic[_E], Input[list[_E], list[Input[Any, _E]]]):
    def __init__(self, inp: Iterable[_E]):
        super().__init__([i if isinstance(i, Input) else BasicInput(i) for i in inp])

    def native(self) -> list[_E]:
        return [e.native() for e in self._inp]

    def chain(self, level=0) -> ListInput[Any]:
        if level < 0:
            raise ValueError
        elif level == 0:
            return ListInput(chain.from_iterable([i._inp for i in self._inp]))
        else:
            return ListInput(i.chain(level - 1) if hasattr(i, 'chain') and callable(getattr(i, 'chain'))
                             else i for i in self._inp)

    def flat(self) -> ListInput[_E] | Input[Any, _E]:
        if len(self._inp) == 1:
            return self._inp[0]
        else:
            return ListInput(i.flat() if hasattr(i, 'flat') and callable(getattr(i, 'flat')) else i for i in self._inp)

    def filter(self, predicate: Callable[[_E | Any], bool], top=False) -> ListInput[_E]:
        if not top and all(isinstance(i, ListInput) for i in self._inp):
            return ListInput(i.filter(predicate) for i in self._inp if isinstance(i, ListInput))
        else:
            return ListInput(i for i in self._inp if predicate(i.native()))

    def filter_type(self, data_type: type):
        return self.filter(lambda e: isinstance(e, data_type))

    _R = TypeVar('_R')

    def map(self, mapper: Callable[[_E], _R] | Mapping[_E, _R]) -> ListInput[_R | ListInput]:
        if not callable(mapper):
            m = mapper

            def mapper(k: _E):
                return m[k] if k in m else k

        return ListInput(i.map(mapper) if isinstance(i, ListInput) else mapper(i._inp) for i in self._inp)

    def int_list(self) -> ListInput[int]:
        return ListInput([
            getattr(i, 'int_list' if hasattr(i, 'int_list') and callable(getattr(i, 'int_list'))
                    else 'int')()
            for i in self._inp
        ])

    def pd(self) -> PandasInput | PandasSeriesInput:
        if all(isinstance(i, Iterable) for i in self._inp):
            return self.pd_records()
        else:
            return self.pd_series()

    def pd_series(self) -> PandasSeriesInput:
        return PandasSeriesInput(pd.Series(self.native()))

    def pd_records(self) -> PandasInput:
        return PandasInput(pd.DataFrame.from_records(self.native()))

    def np(self) -> NumpyInput:
        return NumpyInput(np.array(self.native()))

    def np_int(self) -> NumpyInput:
        return NumpyInput(np.array(self.int_list().native()))

    def __iter__(self) -> Generator[Input[Any, _E], None, None]:
        yield from self._inp

    def __getitem__(self, item) -> Input[Any, _E] | ListInput[_E]:
        if isinstance(item, slice):
            return ListInput(self._inp[item])
        else:
            return self._inp[item]

    def __len__(self):
        return len(self._inp)

    def __getattr__(self, name):
        if all(hasattr(i, name) and callable(getattr(i, name)) for i in self._inp):
            return lambda *args, **kwargs: ListInput([getattr(i, name)(*args, **kwargs) for i in self._inp])
        else:
            raise AttributeError


class MixedListInput(ListInput[Any]):
    def __init__(self, inp: Iterable):
        super().__init__(inp)

    def __getattr__(self, name):
        return lambda *args, **kwargs: ListInput(
            getattr(i, name)(*args, **kwargs) if hasattr(i, name) and callable(getattr(i, name))
            else i for i in self._inp
        )


class StrListInput(ListInput[str]):
    _inp: list[StrInput]

    def __init__(self, inp: Iterable[str]):
        super().__init__([])
        self._inp = [StrInput(i) for i in inp]

    def split(self,
              split_seq: str,
              max_split: int = 0,
              flags: int | re.RegexFlag = 0,
              remove_empty=False) -> ListInput[StrListInput]:
        return ListInput(s.split(split_seq, max_split, flags, remove_empty) for s in self._inp)

    def sections(self,
                 *classes: str,
                 include_no_match=True,
                 remove_empty=True,
                 opt_int=True) -> ListInput[ListInput[str | int]]:
        return ListInput(s.sections(*classes,
                                    include_no_match=include_no_match,
                                    remove_empty=remove_empty,
                                    opt_int=opt_int)
                         for s in self._inp)

    def extract(self,
                *patterns: str,
                include_no_match=True,
                remove_empty=True,
                opt_int=False) -> ListInput[ListInput[str | int]]:
        return ListInput(s.extract(*patterns,
                                   include_no_match=include_no_match,
                                   remove_empty=remove_empty,
                                   opt_int=opt_int)
                         for s in self._inp)

    def filter_int(self):
        return self.opt_int().filter_type(int)

    def __iter__(self) -> Generator[StrInput, None, None]:
        yield from self._inp

    def __getitem__(self, item) -> StrListInput | StrInput:
        if isinstance(item, slice):
            return StrListInput(s.native() for s in self._inp[item])
        else:
            return self._inp[item]


# -------- OTHER INPUTS -------- #

class PandasInput(BasicInput[pd.DataFrame]):
    _inp: pd.DataFrame

    def __init__(self, inp: pd.DataFrame):
        super().__init__(inp)

    def tuples(self, index=False) -> ListInput[tuple]:
        return ListInput(self._inp.itertuples(index=index, name=None))

    def native_tuples(self, index=False):
        return self.tuples(index=index).native()

    def np(self) -> NumpyInput:
        return NumpyInput(self._inp.to_numpy(copy=True))

    def drop_common(self) -> PandasInput:
        return PandasInput(self._inp.loc[:, ~(self._inp == self._inp.iloc[0]).all(axis=0)])


class PandasSeriesInput(BasicInput[pd.Series]):
    _inp: pd.Series

    def __init__(self, inp: pd.Series):
        super().__init__(inp)

    def np(self) -> NumpyInput:
        return NumpyInput(self._inp.to_numpy(copy=True))


class NumpyInput(BasicInput[np.ndarray]):
    _inp: np.ndarray

    def __init__(self, inp: ArrayLike):
        super().__init__(np.array(inp))
