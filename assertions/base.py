""" module for base assertions """

from typing import Union, Literal, List
from abc import ABC, abstractmethod

import pandas as pd
import pandera as pa

from core.exceptions import ValidationError



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
        """ validation of passed args """
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


class FnAssertion(BaseAssertion):
    """ Function Assertion - runs your custom function as assertion """
    name = "FnAssertion"
    def __init__(self, fn: callable, *args:tuple, **kwargs: dict):
        """
        Assertion will be failed if fn throws any exception, otherwise passed
        Parameters
            :param fn: function
            :param args: tuple - positional args for fn
            :param kwargs: dict - keyword args for fn
        """
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def validate(self):
        if not callable(self.fn): raise ValidationError("`fn` must be callable")

    def assertion(self) -> bool:
        try:
            self.fn(*self.args, **self.kwargs)
        except Exception as e:
            msg = f"Assertion Function Failed: '{e}'"
            return self.set_failed(msg)
        else:
            return self.set_passed()