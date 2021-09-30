from typing import List, Optional

from .general import Token, TokenType, KeyWords
from .general.exceptions import IlegalCharException
from .general.position import Position


class Lexer():

    def __init__(self, fn, text) -> None:
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, 0, fn, text)  # Index to self.text
        self.current_token = None  # Current token instance
        self.current_char: Optional[str] = None
        self.advance()

    def advance(self) -> None:
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def skip_whitespace(self):
        while self.current_char() is not None and self.current_char().isspace():
            self.advance()

    def make_number(self) -> Token:
        """Return a (multidigit) number consumed from the input."""
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char.isdigit() or self.current_char == '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1

            num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TokenType.INT, int(num_str), pos_start=pos_start, pos_end=self.pos)

        return Token(TokenType.FLOAT, float(num_str), pos_start=pos_start, pos_end=self.pos)

    def make_identifier(self) -> Token:
        """Return a (multicharacter) identifier consumed from the input."""
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char is not None and (
            self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_'
        ):
            id_str += self.current_char
            self.advance()

        tok_type = TokenType.KEYWORD if id_str in KeyWords._member_names_ else TokenType.IDENTIFIER
        return Token(tok_type, id_str, pos_start=pos_start, pos_end=self.pos)

    def make_tokens(self) -> List[Token]:
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()

            elif self.current_char.isdigit():
                tokens.append(self.make_number())

            elif self.current_char.isalpha() or self.current_char == '_':  # is letter or _
                tokens.append(self.make_identifier())

            elif self.current_char == '+':
                tokens.append(Token(TokenType.PLUS, pos_start=self.pos))
                self.advance()

            elif self.current_char == '-':
                tokens.append(Token(TokenType.MINUS, pos_start=self.pos))
                self.advance()

            elif self.current_char == '*':
                tokens.append(Token(TokenType.MUL, pos_start=self.pos))
                self.advance()

            elif self.current_char == '^':
                tokens.append(Token(TokenType.POW, pos_start=self.pos))
                self.advance()

            elif self.current_char == '/':
                tokens.append(Token(TokenType.DIV, pos_start=self.pos))
                self.advance()

            elif self.current_char == '=':
                tokens.append(Token(TokenType.EQ, pos_start=self.pos))
                self.advance()

            elif self.current_char == '(':
                tokens.append(Token(TokenType.LPAREN, pos_start=self.pos))
                self.advance()

            elif self.current_char == ')':
                tokens.append(Token(TokenType.RPAREN, pos_start=self.pos))
                self.advance()

            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IlegalCharException(pos_start=pos_start,
                                               pos_end=self.pos,
                                               details=f'"{char}"',
                                               )

        tokens.append(Token(TokenType.EOF, pos_start=self.pos))
        return tokens, None
