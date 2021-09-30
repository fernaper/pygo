from dataclasses import dataclass, replace, field


@dataclass
class Position:
    idx: int  # Index
    ln: int  # Line number
    col: int  # Col number
    fn: str = field(repr=False)  # File name
    ftxt: str = field(repr=False)  # File text

    def advance(self, current_char=None) -> 'Position':
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self) -> 'Position':
        return replace(self)
