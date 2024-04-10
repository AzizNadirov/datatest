from typing import Union, Literal, List
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
import pandera as pa

from .exceptions import ValidationError




class BaseAssertion(ABC):
    name: str = "Assertion"
    status: Literal["passed", "failed"] = None
    error_message: str = None

    @abstractmethod
    def assertion(self) -> bool:
        """ assertion method, returns True if the assertion passed, False otherwise. """
        ...

    def set_passed(self) -> bool:
        self.status = "passed"
        return True

    def set_failed(self, error_message: str = None) -> bool:
        """ set status of assertion as failed with message """
        self.status = "failed"
        if error_message:
            self.error_message = error_message
        return False

    def prepare_args(self):
        """ prepare self attributes for assertion, will be run before `assertion` itself """
        pass

    def validate(self):
        pass

    def run(self) -> bool:
        """ run validation, preparation and assertion """
        self.validate()
        self.prepare_args()
        return self.assertion()

    def __str__(self):
        return f"<Assertion {self.name}>"

    def __repr__(self):
        return str(self)
    


class PanderaSchemaAssertion(BaseAssertion):
    """ Pandera DataFrame Schema  """
    name = "PanderaDataFrameSchema"
    def __init__(self, 
                 schema: pa.DataFrameSchema,
                 df: pd.DataFrame):
        self.pa_schema = schema
        self.df = df

    def validate(self):
        """  """
        if not isinstance(self.df, pd.DataFrame): raise ValidationError("`df` must be type of: pd.DataFrame")
        if not isinstance(self.pa_schema, pa.DataFrameSchema): raise ValidationError("`schema` must be type of: pa.DataFrameSchema")

    def assertion(self) -> bool:
        try:
            self.pa_schema.validate(self.df)
        except pa.errors.SchemaError as e:
            return self.set_failed(str(e))
        else:
            return self.set_passed()


class DFHasColumnsAssertion(BaseAssertion):
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

