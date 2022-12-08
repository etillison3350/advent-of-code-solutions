from __future__ import annotations

from numpy.typing import ArrayLike

from input_basic import BasicInput
from input_list import ListInput

import numpy as np
import pandas as pd


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