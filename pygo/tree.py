from dataclasses import dataclass, field
from pygo import Token
from typing import Union

from .general.position import Position


@dataclass
class Node():
    ...


@dataclass
class NumberNode(Node):
    tok: Token
    pos_start: Position = field(default=None)
    pos_end: Position = field(default=None)

    def __post_init__(self):
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self) -> str:
        return f'{self.tok}'


@dataclass
class VarAssignNode(Node):
    tok: Token
    value_node: str

    pos_start: Position = field(default=None)
    pos_end: Position = field(default=None)

    def __post_init__(self):
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end


@dataclass
class VarAccessNode(Node):
    tok: Token
    pos_start: Position = field(default=None)
    pos_end: Position = field(default=None)

    def __post_init__(self):
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end


@dataclass
class BinOpNode(Node):
    left_node: Union['BinOpNode', NumberNode]
    op_tok: Token
    right_node: Union['BinOpNode', NumberNode]
    pos_start: Position = field(default=None)
    pos_end: Position = field(default=None)

    def __post_init__(self):
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self) -> str:
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


@dataclass
class UnaryOpNode(Node):
    op_tok: Token
    node: Union['BinOpNode', NumberNode]
    pos_start: Position = field(default=None)
    pos_end: Position = field(default=None)

    def __post_init__(self):
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self) -> str:
        return f'({self.op_tok}, {self.node})'
