from __future__ import annotations

from typing import Any, Callable, Generator, Iterable, Mapping
from typing import Generic, TypeVar

from input_basic import Input, BasicInput, StrInput
from input_extern import PandasInput, PandasSeriesInput, NumpyInput

from itertools import chain
import re

import numpy as np
import pandas as pd


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