from ..context import Context
from ..utils.string_with_arrows import string_with_arrows


class InterpreterException(Exception):

    def __init__(self, error_name='Interpreter Error', **kwargs):
        self.error_name = error_name
        self.pos_start = kwargs.get('pos_start')
        self.pos_end = kwargs.get('pos_end')
        self.details = kwargs.get('details')

        super().__init__(self.as_str())

    def as_str(self) -> str:
        details = f': {self.details}' if self.details else ''

        return (
            f'{self.error_name}{details}\n' +
            f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}\n\n' +
            string_with_arrows(self.pos_start.ftxt,
                               self.pos_start, self.pos_end)
        )


class IlegalCharException(InterpreterException):
    def __init__(self, **kwargs):
        super().__init__('Ilegal Character', **kwargs)


class InvalidSintaxError(InterpreterException):
    def __init__(self, **kwargs):
        super().__init__('Invalid Syntax', **kwargs)


class NoVisitMethod(InterpreterException):
    def __init__(self, node, **kwargs):
        super().__init__(
            f'No visit_{type(node).__name__} method defined', **kwargs)

    def as_str(self) -> str:
        return str(self)


class RTException(InterpreterException):
    def __init__(self, **kwargs):
        self.context: Context = kwargs.pop('context', None)
        super().__init__('Runtime error', **kwargs)

    def as_str(self) -> str:
        details = f': {self.details}' if self.details else ''

        return (
            self.generate_traceback() +
            f'{self.error_name}{details}\n\n' +
            string_with_arrows(self.pos_start.ftxt,
                               self.pos_start, self.pos_end)
        )

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        context = self.context

        while context:
            result += f'  File {pos.fn}, line {pos.ln + 1}, in {context.display_name}\n'
            pos = context.parent_entry_pos
            context = context.parent

        return 'Traceback (most recent call last):\n' + result
