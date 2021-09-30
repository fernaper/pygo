from dataclasses import dataclass, field
from typing import Callable, List, Tuple, Optional
from pygo import Token, TokenType
from pygo.tree import BinOpNode, NumberNode, UnaryOpNode, Node, VarAccessNode, VarAssignNode
from pygo.general.exceptions import InterpreterException, InvalidSintaxError


@dataclass
class ParserResult():
    node: Optional[Node] = None
    error: Optional[InterpreterException] = None
    advance_count: int = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res: 'ParserResult') -> Node:
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node: Node) -> 'ParserResult':
        self.node = node
        return self

    def failure(self, error: InterpreterException) -> 'ParserResult':
        if not self.error or self.advance_count == 0:
            self.error = error
        return self


@dataclass
class Parser():
    tokens: List[Token]
    tok_idx: int = -1
    current_tok: Token = field(default=None)

    def __post_init__(self):
        self.advance()

    def advance(self) -> Token:
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def get_next_tok(self) -> Optional[Token]:
        if self.tok_idx + 1 < len(self.tokens):
            return self.tokens[self.tok_idx + 1]

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.token_type != TokenType.EOF:
            return res.failure(InvalidSintaxError(
                pos_start=self.current_tok.pos_start.copy(),
                pos_end=self.current_tok.pos_end.copy(),
                details='Expected "+", "-", "*", "/" or "^"'
            ))
        return res

    def atom(self) -> ParserResult:
        res = ParserResult()
        tok = self.current_tok

        if tok.token_type in (TokenType.INT, TokenType.FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.token_type == TokenType.IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.token_type == TokenType.LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.token_type == TokenType.RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSintaxError(
                    pos_start=self.current_tok.pos_start.copy(),
                    pos_end=self.current_tok.pos_end.copy(),
                    details='Expected ")"'
                ))

        return res.failure(InvalidSintaxError(
            pos_start=tok.pos_start.copy(),
            pos_end=tok.pos_end.copy(),
            details='Expected int, float, identifier, "+", "-" or "("'
        ))

    def term(self) -> ParserResult:
        return self.bin_op(self.factor, (TokenType.MUL, TokenType.DIV))

    def power(self) -> ParserResult:
        return self.bin_op(self.atom, (TokenType.POW, ), self.factor)

    def factor(self) -> ParserResult:
        res = ParserResult()
        tok = self.current_tok

        if tok.token_type in (TokenType.PLUS, TokenType.MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def expr(self) -> ParserResult:
        res = ParserResult()
        if self.current_tok.matches(TokenType.IDENTIFIER):
            var_name = self.current_tok
            next_tok = self.get_next_tok()
            if next_tok is not None and next_tok.token_type == TokenType.EQ:
                res.register_advancement()
                self.advance()  # Advance the Identifier
                res.register_advancement()
                self.advance()  # Advance the equals
                expr = res.register(self.expr())
                if res.error:
                    return res
                return res.success(VarAssignNode(var_name, expr))
        return self.bin_op(self.term, (TokenType.PLUS, TokenType.MINUS))

    def bin_op(self, func_a: Callable[[], Node],
               ops: Tuple[Token], func_b: Callable[[], Node] = None) -> ParserResult:
        if func_b is None:
            func_b = func_a
        res = ParserResult()
        left = res.register(func_a())

        if res.error:
            return res

        while self.current_tok.token_type in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res

            left = BinOpNode(left, op_tok, right)

        return res.success(left)
