from typing import List, Tuple

from .context import Context
from .general.exceptions import InterpreterException
from .general.token import Token, TokenType
from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser
from .symbol_table import SymbolTable
from .version import __version__


global_symbol_table = SymbolTable()


def run(fn: str, code: str) -> Tuple[List[Token], InterpreterException]:
    if not code:
        return [], None
    lexer = Lexer(fn, code)
    tokens, error = lexer.make_tokens()

    if error:
        return None, error

    # Generate Abstract Sintax Tree (AST)
    parser = Parser(tokens)
    ast = parser.parse()

    if ast.error:
        return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
