from dataclasses import dataclass
from enum import auto, Enum
from typing import Any

from pygo.general.position import Position


class KeyWords(Enum):
    ...


class TokenType(Enum):
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    POW = auto()
    LPAREN = auto()
    RPAREN = auto()
    MODULE = auto()
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    EQ = auto()
    IDENTIFIER = auto()
    METHOD = auto()
    IF = auto()
    ELSE_IF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    EOF = auto()


@dataclass
class Token():
    token_type: TokenType
    value: Any = None
    pos_start: Position = None
    pos_end: Position = None

    def __post_init__(self):
        if self.pos_start:
            self.pos_start = self.pos_start.copy()
            if not self.pos_end:
                self.pos_end = self.pos_start.copy()
                self.pos_end.advance()

    def __str__(self) -> str:
        return f'T_{self.token_type.name}{":"+str(self.value) if self.value is not None else ""}'

    def __repr__(self) -> str:
        return self.__str__()

    def matches(self, token_type, value=None):
        return self.token_type == token_type and (self.value == value or value == None)
