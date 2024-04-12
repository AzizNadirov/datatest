from typing import List, Dict

from assertions.base import BaseAssertion
from .exceptions import ValidationError
import colorama


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
                print(colorama.Fore.GREEN + f"\t{i}|{assertion.name}|: [{assertion.status}]")
            else:
                print(colorama.Fore.RED + f"\t{i}|{assertion.name}|: [{assertion.status}] -> {assertion.error_message}")
        n_passed = len([a for a in run_result.values() if a.status == 'passed'])
        n_all = len(run_result)
        n_failed = n_all - n_passed
        if n_failed == 0:
            print(colorama.Fore.GREEN + f"Successfully ran [{n_passed}/{n_all}] assertions")
        
        elif n_passed > n_failed:
            print(colorama.Fore.YELLOW + f"Successfully ran [{n_passed}/{n_all}] assertions")
        
        else:
            print(colorama.Fore.RED + f"Successfully ran [{n_passed}/{n_all}] assertions")


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
