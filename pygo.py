import readline
import pygo

from datetime import datetime
from pygo.general.exceptions import InterpreterException


def shell():
    print(
        f'PyGo {pygo.__version__} ({datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")})')

    try:
        while True:
            try:
                text = input('>>> ')
                tokens, error = pygo.run('<stdin>', text)

                if error:
                    print(error)
                    continue
                print(tokens)

            except KeyboardInterrupt:
                print('\nKeyboardInterrupt')

    except EOFError:
        print('')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('code', default=None, nargs='?',
                        help='Code text or file to interpret.')
    parser.add_argument('-s', '--str', action='store_true',
                        help='If passed, it means that it is the code itself as a string, if not, it is the path to the file.')

    args = parser.parse_args()

    code = args.code
    fn = '<stdin>'
    if args.code and not args.str:
        fn = args.code
        with open(args.code, 'r') as f:
            code = f.read()

    if not code:
        shell()

    else:
        pygo.run(fn, code)
