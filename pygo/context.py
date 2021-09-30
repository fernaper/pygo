from dataclasses import dataclass

if (lambda: False)():
    from .symbol_table import SymbolTable


@dataclass
class Context():
    display_name: str
    parent: 'Context' = None
    parent_entry_pos: int = None
    symbol_table: 'SymbolTable' = None
