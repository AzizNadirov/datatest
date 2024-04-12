""" module for assertions on pandas Series """

from typing import Union, List, Sequence

import pandas as pd
import numpy as np

from assertions.base import BaseAssertion
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
    

class InColumnAssertion(BaseAssertion):
    """  """
    name = "InColumnAssertion"

    def __init__(self, 
                 column: pd.Series,
                 values: Union[Sequence, pd.Series]):
        """ aseerts `column.isin(values).sum() > 0` """
        self.column = column
        self.values = values

    def validate(self):
        valid_dtypes_values = (pd.Series, pd.Index, tuple, list, np.ndarray)
        if not isinstance(self.column, pd.Series): raise ValidationError("`column` must be type of: pd.Series")
        if not isinstance(self.values, valid_dtypes_values): 
            raise ValidationError(f"`values` must be type of: {valid_dtypes_values}")

    def assertion(self) -> bool:
        if (self.column.isin(self.values)).sum() > 0:
            return self.set_passed()
        
        values_not_in = list(self.column.loc[~self.column.isin(self.values)].unique())
        if len(values_not_in) > 20:
            values_not_in = ", ".join(values_not_in[:20]) + ", ..."
        else:
            values_not_in = ", ".join(values_not_in)

        return self.set_failed(f"Column does not contain values in list: '{values_not_in}'")
    

class HasNoDuplicatesAssertion(BaseAssertion):
    """  """
    name = "HasNoDuplicatesAssertion"

    def __init__(self, 
                 column: pd.Series):
        """ aseerts `column.duplicated().sum() == 0` """
        self.column = column

    def validate(self):
        if not isinstance(self.column, pd.Series): raise ValidationError("`column` must be type of: pd.Series")

    def assertion(self) -> bool:
        if self.column.duplicated().sum() == 0:
            return self.set_passed()
        
        duplicateds = {key: value for key, value in self.column.value_counts().to_dict().items() if value > 1}
        return self.set_failed(f"Column contains duplicates: \n\t{duplicateds}")
    

class HasSameIndexAssertion(BaseAssertion):
    name = "HasSameIndexAssertion"

    def __init__(self, 
                 column1: pd.Series,
                 column2: pd.Series):
        """ aseerts `column1.index.equals(column2.index)` """
        self.column1 = column1
        self.column2 = column2

    def validate(self):
        if not isinstance(self.column1, pd.Series): raise ValidationError("`column1` must be type of: pd.Series")
        if not isinstance(self.column2, pd.Series): raise ValidationError("`column2` must be type of: pd.Series")

    def assertion(self) -> bool:
        if self.column1.index.equals(self.column2.index):
            return self.set_passed()
        
        return self.set_failed(f"Column1: {self.column1.index} and Column2: {self.column2.index} have different index")
    

class HasSameDataAssertion(BaseAssertion):
    name = "HasSameDataAssertion"

    def __init__(self, 
                 column1: pd.Series,
                 column2: pd.Series):
        """ aseerts `column1.equals(column2)` """
        self.column1 = column1
        self.column2 = column2

    def validate(self):
        if not isinstance(self.column1, pd.Series): raise ValidationError("`column1` must be type of: pd.Series")
        if not isinstance(self.column2, pd.Series): raise ValidationError("`column2` must be type of: pd.Series")

    def assertion(self) -> bool:
        if (self.column1.values == self.column2.values).all():
            return self.set_passed()
        
        return self.set_failed(f"Column1: {self.column1} and Column2: {self.column2} have different data")
    

class AreSomeAssertion(BaseAssertion):
    name = "AreSomeAssertion"

    def __init__(self, 
                 column1: pd.Series,
                 column2: pd.Series):
        """ aseerts `column1.equals(column2)` """
        self.column1 = column1
        self.column2 = column2

    def validate(self):
        if not isinstance(self.column1, pd.Series): raise ValidationError("`column1` must be type of: pd.Series")
        if not isinstance(self.column2, pd.Series): raise ValidationError("`column2` must be type of: pd.Series")

    def assertion(self) -> bool:
        if self.column1.equals(self.column2):
            return self.set_passed()
        
        return self.set_failed(f"Column1: {self.column1} and Column2: {self.column2} are different")
    

class AreSameLenAssertion(BaseAssertion):
    name = "AreSameLen"

    def __init__(self, 
                 column1: Union[pd.Series, np.ndarray, list, tuple, pd.Index],
                 column2: Union[pd.Series, np.ndarray, list, tuple, pd.Index]):
        """ aseerts `len(column1) == len(column2)` """
        self.column1 = column1
        self.column2 = column2

    def validate(self):
        valid_types = (pd.Series, pd.Index, np.ndarray, list, tuple)
        if not isinstance(self.column1, valid_types): raise ValidationError(f"`column1` must be type of: {valid_types}")
        if not isinstance(self.column2, valid_types): raise ValidationError(f"`column2` must be type of: {valid_types}")

    def assertion(self) -> bool:
        if len(self.column1) == len(self.column2):
            return self.set_passed()
        
        return self.set_failed(f"Column1: {len(self.column1)} and Column2: {len(self.column2)} are different")
    

class LenIsAssertion(BaseAssertion):
    name = "LenIs"

    def __init__(self, 
                 column: Union[pd.Series, np.ndarray, list, tuple, pd.Index],
                 length: int):
        """ aseerts `len(column) == length` """
        self.column = column
        self.length = length

    def validate(self):
        valid_types = (pd.Series, pd.Index, np.ndarray, list, tuple)
        if not isinstance(self.column, valid_types): raise ValidationError(f"`column` must be type of: {valid_types}")
        if not isinstance(self.length, int) and self.length < 0: raise ValidationError("`length` must be type of: int")

    def assertion(self) -> bool:
        if len(self.column) == self.length:
            return self.set_passed()
        
        return self.set_failed(f"Column: {len(self.column)} has different length: {self.length}")

