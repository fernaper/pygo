from dataclasses import dataclass

from .general.exceptions import InterpreterException
from .parser import ParserResult


@dataclass
class RTResult():
    value: int = None
    error: InterpreterException = None

    def register(self, res: ParserResult):
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value) -> 'RTResult':
        self.value = value
        return self

    def failure(self, error) -> 'RTResult':
        self.error = error
        return self
