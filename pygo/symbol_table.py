from .general.number import Number

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class SymbolTable():
    symbols: Dict[str, Number] = field(default_factory=dict)
    parent: Optional['SymbolTable'] = None

    def get(self, name: str) -> Number:
        value = self.symbols.get(name)
        if value is None and self.parent is not None:
            return self.parent.get(name)
        return value

    def set(self, name: str, value: Number) -> None:
        self.symbols[name] = value

    def remove(self, name: str) -> None:
        del self.symbols[name]
