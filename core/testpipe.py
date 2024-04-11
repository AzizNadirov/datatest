from typing import List, Dict

from assertions.base import BaseAssertion
from .exceptions import ValidationError


class TestPipe:
    """ Pipe of Sequence assertions """
    def __init__(self, name: str, assertions: List[BaseAssertion]):
        self.assertions = assertions
        self.name = name
        self.__validate()

    
    def _echo(self, run_result: Dict[int, BaseAssertion]) -> None:
        print(f"[{self.name}]: Running assertions")
        for i, assertion in run_result.items():
            if assertion.status == "passed":
                print(f"\t{i}|{assertion.name}|: [{assertion.status}]")
            else:
                print(f"\t{i}|{assertion.name}|: [{assertion.status}] -> {assertion.error_message}")

        print(f"Successfully ran [{len([a for a in run_result.values() if a.status == 'passed'])}/{len(run_result)}] assertions")


    def __validate(self):
        # validate assertions
        for assertion in self.assertions:
            if not isinstance(assertion, BaseAssertion):
                raise ValidationError(f"Assertion must be instance of subclass `BaseAssertion`, but got: `{type(assertion)}`")
    
    def run(self):
        run_result = {}
        for i, assertion in enumerate(self.assertions, start=1):
            assertion.run()
            run_result[i] = assertion

        self._echo(run_result)
        print(f"Done")

    
    def __repr__(self):
        tests = [str(a) for a in self.assertions]
        return f"<{self.__class__.__name__} {self.name}: {tests}>"
    
    def __str__(self):
        tests = [str(a.name) for a in self.assertions]
        return f"{self.__class__.__name__} {self.name}: {tests}"
