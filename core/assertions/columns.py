""" module for assertions on pandas Series """

from typing import Union, List, Sequence

import pandas as pd
import numpy as np

from core.assertions.base import BaseAssertion
from core.exceptions import ValidationError


class NotInColumnAssertion(BaseAssertion):
    """  """
    name = "NotInColumnAssertion"

    def __init__(self, 
                 column: pd.Series,
                 values: Union[Sequence, pd.Series]):
        """ aseerts `(~column.isin(values)).sum() == 0` """
        self.column = column
        self.values = values

    def validate(self):
        valid_dtypes_values = (pd.Series, pd.Index, tuple, list, np.ndarray)
        if not isinstance(self.column, pd.Series): raise ValidationError("`column` must be type of: pd.Series")
        if not isinstance(self.values, valid_dtypes_values): 
            raise ValidationError(f"`values` must be type of: {valid_dtypes_values}")

    def assertion(self) -> bool:
        if (self.column.isin(self.values)).sum() == 0:
            return self.set_passed()
        
        values_in = list(self.column.loc[self.column.isin(self.values)].unique())
        if len(values_in) > 20:
            values_in = ", ".join(values_in[:20]) + ", ..."
        else:
            values_in = ", ".join(values_in)

        return self.set_failed(f"Column contains values in list: '{values_in}'")