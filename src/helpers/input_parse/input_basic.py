from __future__ import annotations

from typing import Callable, Generator, Mapping, Optional, Sequence
from typing import Generic, TypeVar

from abc import ABC, abstractmethod

from input_list import ListInput, MixedListInput, StrListInput
from input_extern import NumpyInput

from itertools import chain, pairwise
import json
import re


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

    def splitlines(self):
        return self.split('\n')

    def split_paragraphs(self):
        return self.split('\n\n')

    def strip(self):
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