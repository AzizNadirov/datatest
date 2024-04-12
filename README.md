# DataTest

Micro library for write unittest-like tests(assertions) for Data Science projects. Contains pandas.Series and pandas.DataFrame related assertions. Also, can handle [pandera](https://pandera.readthedocs.io/en/stable/) schemas for assertion testing.

## Assertions: `datatest.assertions`

Assertions have three modules:

- `datatest.assertions.base`: base assertions
- `datatest.assertions.columns`: assertions on pandas Series
- `datatest.assertions.df`: assertions on pandas DataFrames

### Base Assertions: `datatest.assertions.base`

There are 3 main Assertion classes that can be helpfull:

- `BaseAssertion`: abstract base class for all assertions. You can inherite this class for create your own assertions.
- `FnAssertion`: assertion based on the custom function.
- `PanderaSchemaAssertion`: assertion on pandas DataFrame with [pandera](https://pandera.readthedocs.io/en/stable/) schema

#### abstract BaseAssertion

```python
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

    def run(self) -> bool:
        """ run validation, preparation and assertion """
        self.validate()
        self.prepare_args()
        return self.assertion()
```

For creating your own assertions you have to inherite `BaseAssertion` and implement `assertion` method.
The method have to return call of `set_passed` or `set_failed` method, and they return boolean. `set_failed`
takes a string with error message. This message will be displayed if the assertion is failed and should be a little informative.
Also, you can implement `validate` and `prepare_args` methods. First, will be called `validate` method, then `prepare_args`, where you can do some preparation for the assertion.
Finally, you have to implement `assertion` method. Here is an example:

```python
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
```

`run` method of the assertions will run `validate`, `prepare_args` and `assertion` methods sequentially.

#### FnAssertion

`FnAssertion(fn: callable, *args:tuple, **kwargs: dict)`  - assertion based on the custom `fn` function.
`args` and `kwargs` are positional and keyword arguments that will be passed to the `fn` function. Assertion will be failed if `fn`
raises any exception, otherwise passed.

```python
def fn(df: pd.DataFrame):
    if df['numeric'].mean() > 100:
        pass
    else:
        raise AssertionError("Mean is less than 50")

fna = FnAssertion(fn=fn, df=df)
```

#### PanderaSchemaAssertion

`PanderaSchemaAssertion(schema: pa.DataFrameSchema, df: pd.DataFrame)` - assertion on pandas DataFrame with [pandera](https://pandera.readthedocs.io/en/stable/) schema.
Pandera gives you rich set of validation rules for pandas DataFrame. You can use it as validation tool here.

```python
df_schema = pa.DataFrameSchema({
                                "site_name": pa.Column(str, checks=pa.Check(lambda site_name: site_name.str.isalpha())),
                                "site_url": pa.Column(str, checks=pa.Check(validate_url))})
pa1 = PanderaSchemaAssertion(df_schema, df)
```

In the example above, `df` must be pandas DataFrame and `df_schema` must be pandera schema. Assertion will be failed if `df_schema` failed schema validation by pandera, otherwise passed.

## testdata.core.TestPipe

`testdata.core.TestPipe` - runs assertions sequentially.

```python
pipe = TestPipe(name: str, assertions: List[BaseAssertion])
pipe.run()
```

`pipe.run()` will run pipeline, and assertions will be run sequentially.Finally, you will see printed result - passed/failed assertions and error messages.

```bash
[test_pipe]: Running assertions
	1|DFHasColumns|: [passed]
	2|DFHasColumns|: [passed]
	3|DFHasColumns|: [failed] -> Columns: '['domain', 'numeric']' are in df, but not in your list: ['site_name', 'site_url']
	4|PanderaDataFrameSchema|: [passed]
	5|FnAssertion|: [failed] -> Assertion Function Failed: 'Mean is less than 50'
Successfully ran [3/5] assertions
Done
```

## Installation

```bash
pip install git+https://github.com/AzizNadirov/datatest.git
```

## TODO

- write azure-pipeline CI/CD pipeline
- mb logging
- detailed tests for tests `:)`
- mb integrate python' unittest test cases...