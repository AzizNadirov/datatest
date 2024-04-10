""" module for assertions on pandas dataframes """

from typing import Union, Literal, List
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from core.exceptions import ValidationError
from .base import BaseAssertion





class HasColumnsAssertion(BaseAssertion):
    name = "DFHasColumns"

    def __init__(self,
                 df: Union[pd.DataFrame, pd.Index, List[str], np.ndarray],
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
        self.df_cols = None

    def prepare_args(self) -> None:
        # convert columns into a list
        if isinstance(self.columns, pd.Index):
            self.columns = self.columns.to_list()

        if isinstance(self.df, pd.DataFrame):
            self.df_cols = self.df.columns.tolist()

        elif isinstance(self.df, (pd.Index, pd.Series)):
            self.df_cols = self.df.to_list()

        elif isinstance(self.df, (list, tuple, np.ndarray)):
            self.df_cols = list(self.df)

        else:
            raise ValidationError("df must be type of: pd.DataFrame, pd.Index, pd.Series, np.ndarray, list or tuple")

    def assertion(self):
        not_in_df = set(self.columns) - set(self.df_cols)
        if not self.strict:
            if not not_in_df:
                return self.set_passed()
            else:
                return self.set_failed(f"Columns: '{list(not_in_df)}' not in df: {self.df_cols}.")
        else:
            not_in_columns = set(self.df_cols) - set(self.columns)
            if not not_in_df:
                if not not_in_columns:
                    return self.set_passed()
                else:
                    msg = f"Columns: '{list(not_in_columns)}' are in df, but not in your list: {self.columns}"
                    return self.set_failed(msg)
            else:
                msg = f"Columns: '{list(not_in_df)}' not in df: {self.df_cols}"
                return self.set_failed(msg)




