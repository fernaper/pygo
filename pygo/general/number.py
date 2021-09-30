from dataclasses import dataclass, replace
from typing import Optional, Tuple, Union

from .exceptions import RTException
from .position import Position
from ..context import Context


@dataclass
class Number():
    value: Union[int, float]
    pos_start: Position = None
    pos_end: Position = None
    context: Context = None

    def set_pos(self, pos_start: Position = None, pos_end: Position = None) -> 'Number':
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context: Context = None) -> 'Number':
        self.context = context
        return self

    def added_to(self, other) -> Tuple['Number', None]:
        if isinstance(other, Number):
            return Number(self.value + other.value, context=self.context), None

    def subbed_by(self, other) -> Tuple['Number', None]:
        if isinstance(other, Number):
            return Number(self.value - other.value, context=self.context), None

    def multed_by(self, other) -> Tuple['Number', None]:
        if isinstance(other, Number):
            return Number(self.value * other.value, context=self.context), None

    def divided_by(self, other) -> Tuple['Number', Optional[RTException]]:
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTException(pos_start=other.pos_start,
                                         pos_end=other.pos_end,
                                         details='Divison by zero',
                                         context=self.context
                                         )
            return Number(self.value / other.value, context=self.context), None

    def powed_by(self, other) -> Tuple['Number', None]:
        if isinstance(other, Number):
            return Number(self.value ** other.value, context=self.context), None

    def __repr__(self) -> str:
        return f'{self.value}'

    def copy(self) -> 'Number':
        return replace(self)
