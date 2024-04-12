""" module for assertions on pandas dataframes """

from typing import Union, Literal, List

import numpy as np
import pandas as pd

from core.exceptions import ValidationError
from .base import BaseAssertion




class HasColumnsAssertion(BaseAssertion):
    name = "DFHasColumns"

    def __init__(self,
                 df: pd.DataFrame,
                 columns: Union[List[str], pd.Index],
                 strict: bool = False
                 ):
        """ df pandas dataframe must have columns listed in `columns` list or columns of the df itself
            :param df: pandas dataframe
            :param columns: columns list
            :param strict: if `True`, will raise error if there is any columns not listed in `columns`, defaults to `False`
        """
        assert isinstance(df, pd.DataFrame), "df must be of type pd.DataFrame"
        self.df = df
        self.columns = columns
        self.strict = strict

    def validate(self):
        if not isinstance(self.df, pd.DataFrame): raise ValidationError(f"{self.df} must be of type pd.DataFrame")
        if not isinstance(self.columns, (List[str], pd.Index)): raise ValidationError(f"{self.df} must be of type pd.DataFrame")

    def prepare_args(self) -> None:
        # convert columns into a list
        if isinstance(self.columns, pd.Index):
            self.columns = self.columns.to_list()

    def assertion(self):
        df_cols = self.df.columns.to_list()
        not_in_df = set(self.columns) - set(df_cols)
        if not self.strict:
            if not not_in_df:
                return self.set_passed()
            else:
                return self.set_failed(f"Columns: '{list(not_in_df)}' not in df: {df_cols}.")
        else:
            not_in_columns = set(df_cols) - set(self.columns)
            if not not_in_df:
                if not not_in_columns:
                    return self.set_passed()
                else:
                    msg = f"Columns: '{list(not_in_columns)}' are in df, but not in your list: {self.columns}"
                    return self.set_failed(msg)
            else:
                msg = f"Columns: '{list(not_in_df)}' not in df: {df_cols}"
                return self.set_failed(msg)


class HasSameColumnsAssertion(BaseAssertion):
    name = "HasSameColumns"

    def __init__(self,
                 df1: Union[pd.DataFrame, pd.Index, List[str], np.ndarray],
                 df2: Union[pd.DataFrame, pd.Index, List[str], np.ndarray]
                 ):
        """ df1 and df2 pandas dataframes must have same columns
            :param df1: pandas dataframe
            :param df2: pandas dataframe
        """
        assert isinstance(df1, pd.DataFrame), "df1 must be of type pd.DataFrame"
        assert isinstance(df2, pd.DataFrame), "df2 must be of type pd.DataFrame"
        self.df1 = df1
        self.df2 = df2

    def prepare_args(self) -> None:
        pass

    def assertion(self):
        diff = set(self.df1.columns.to_list()).symmetric_difference(set(self.df2.columns.to_list()))
        if diff:
            return self.set_passed()
        else:
            
            return self.set_failed(f"df1: {self.df1.columns} and df2: {self.df2.columns} have different columns: {diff}")


class HasSameIndexAssertion(BaseAssertion):
    name = "HasSameIndex"

    def __init__(self,
                 df1: Union[pd.DataFrame, pd.Index, List[str], np.ndarray],
                 df2: Union[pd.DataFrame, pd.Index, List[str], np.ndarray]
                 ):
        """ df1 and df2 pandas dataframes must have the same index
            :param df1: pandas dataframe
            :param df2: pandas dataframe
        """
        assert isinstance(df1, pd.DataFrame), "df1 must be of type pd.DataFrame"
        assert isinstance(df2, pd.DataFrame), "df2 must be of type pd.DataFrame"
        self.df1 = df1
        self.df2 = df2

    def prepare_args(self) -> None:
        pass

    def assertion(self):
        if self.df1.index.equals(self.df2.index):
            return self.set_passed()
        else:
            return self.set_failed(f"df1: {self.df1.index} and df2: {self.df2.index} have different index")
        

class HasSameDataAssertion(BaseAssertion):
    name = "HasSameData"

    def __init__(self,
                 df1: Union[pd.DataFrame, pd.Index, List[str], np.ndarray],
                 df2: Union[pd.DataFrame, pd.Index, List[str], np.ndarray]
                 ):
        """ df1 and df2 pandas dataframes must have the same data
            :param df1: pandas dataframe
            :param df2: pandas dataframe
        """
        assert isinstance(df1, pd.DataFrame), "df1 must be of type pd.DataFrame"
        assert isinstance(df2, pd.DataFrame), "df2 must be of type pd.DataFrame"
        self.df1 = df1
        self.df2 = df2

    def prepare_args(self) -> None:
        pass

    def assertion(self):
        if set(self.df1.columns.to_list()) == set(self.df2.columns.to_list()) and\
                (self.df1.values == self.df2.values).all():
            return self.set_passed()
        else:
            return self.set_failed(f"df1: {self.df1} and df2: {self.df2} have different data")


class HasSameShape(BaseAssertion):
    name = "HasSameShape"

    def __init__(self,
                 df1: Union[pd.DataFrame, pd.Index, List[str], np.ndarray],
                 df2: Union[pd.DataFrame, pd.Index, List[str], np.ndarray]
                 ):
        """ df1 and df2 pandas dataframes must have the same shape
            :param df1: pandas dataframe
            :param df2: pandas dataframe
        """
        assert isinstance(df1, pd.DataFrame), "df1 must be of type pd.DataFrame"
        assert isinstance(df2, pd.DataFrame), "df2 must be of type pd.DataFrame"
        self.df1 = df1
        self.df2 = df2

    def prepare_args(self) -> None:
        pass

    def assertion(self):
        if self.df1.shape == self.df2.shape:
            return self.set_passed()
        else:
            return self.set_failed(f"df1: {self.df1.shape} and df2: {self.df2.shape} have different shape")
        

class ShapeIs(BaseAssertion):
    name = "ShapeIs"

    def __init__(self,
                 df: pd.DataFrame,
                 shape: tuple
                 ):
        """ df pandas dataframe must have shape
            :param df: pandas dataframe
            :param shape: shape. if one of the dimensions is -1, then won't check for that dimension
        """
        assert isinstance(df, pd.DataFrame), "df must be of type pd.DataFrame"
        self.df = df
        self.shape = shape

    def prepare_args(self) -> None:
        pass

    def assertion(self):
        if len(self.df.shape) != len(self.shape):
            return self.set_failed(f"df: {self.df.shape} has different shape: {self.shape}")
        else:
            for df_ax, shape_ax in zip(self.df.shape, self.shape):
                if df_ax != shape_ax and shape_ax != -1:
                    return self.set_failed(f"df: {self.df.shape} has different shape: {self.shape}")
                
            return self.set_passed()
        

class AreSomeAssertion(BaseAssertion):
    name = "AreSome"

    def __init__(self, df1: pd.DataFrame, df2: pd.DataFrame):
        """ df1 and df2 pandas dataframes must have the some elements
            :param df1: pandas dataframe
            :param df2: pandas dataframe
        """
        assert isinstance(df1, pd.DataFrame), "df1 must be of type pd.DataFrame"
        assert isinstance(df2, pd.DataFrame), "df2 must be of type pd.DataFrame"
        self.df1 = df1
        self.df2 = df2

    def prepare_args(self) -> None:
        pass

    def assertion(self):
        if self.df1.equals(self.df2):
            return self.set_passed()
        else:
            return self.set_failed(f"df1: {self.df1} and df2: {self.df2} have different data")
        
    