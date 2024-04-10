from typing import Union, Literal, List
from abc import ABC, abstractmethod

from dataclasses import dataclass
import pandas as pd


class BaseAssertion(ABC):
    status: Literal["passed", "failed"]
    error_message: str

    @abstractmethod
    def assertion(self, *args, **kwargs):
        ...

    def set_passed(self):
        self.status = "passed"

    def set_failed(self, error_message: str=None):
        self.status = "failed"
        if error_message:
            self.error_message = error_message

    def prepare_args(self):
        pass

    def run(self):
        self.prepare_args()


class DFHasColumns(BaseAssertion):
    def __init__(self,
                 df: Union[pd.DataFrame, pd.Index],
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

    def prepare_args(self):
        # convert columns into a list
        if isinstance(self.columns, pd.Index):
            self.columns = self.columns.to_list()

    def assertion(self, *args):
        if not self.strict:
            not_in_df = set(self.columns) - set(self.df.columns)

            if set(self.columns).issubset(set(self.df.columns.to_list())):
                return self.set_passed()
            else:

                return self.set_failed(f"")
        else:
            pass




