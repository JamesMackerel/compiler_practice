from lextable import LexTable
from source import Source
from compileerror import CompileError

# all key words are in lower case, operators are in upper case
TYPE = {
    'begin': 1,
    'end': 2,
    'if': 3,
    'then': 4,
    'else': 5,
    'ID': 6,
    'INT': 7,
    '<': 8,
    '<=': 9,
    '=': 10,
    '<>': 11,
    '>': 12,
    '>=': 13,
    '+': 14,
    '-': 15,
    '*': 16,
    '/': 17,
    ':=': 18,
    'var': 19,
    'while': 20,
    'do': 23,
    ';': 24,  # End Of Sentence
    '(': 27,  # (
    ')': 28  # )
}


def lex(source: Source) -> LexTable:
    """
    :param source_path: path to the source code file
    :return: List of tuple, which stores key word and identifiers and its type
    """
    lex_table = LexTable(source)  # type:LexTable
    while True:
        ch = source.get()
        if ch in ['\n', '\r', ' ']:
            continue
        if ch is None:
            return lex_table

        buffer = []
        if ch.isalpha():
            buffer.append(ch)

            ch = source.get()
            while ch.isalnum():
                buffer.append(ch)
                ch = source.get()

            source.back()

            try:
                res = (TYPE[''.join(buffer).lower()], ''.join(buffer).lower())
            except KeyError:
                res = (TYPE['ID'], ''.join(buffer))
            lex_table.append(res)

        elif ch.isdigit():
            buffer.append(ch)
            ch = source.get()
            while ch.isdigit():
                buffer.append(ch)
                ch = source.get()

            source.back()
            lex_table.append((TYPE['INT'], int(''.join(buffer))))

        else:  # not a identifier or number
            if ch == '<':
                ch = source.get()
                if ch == '=':
                    lex_table.append((TYPE['<='], ch))
                elif ch == '>':
                    lex_table.append((TYPE['<>'], '<>'))
                else:
                    source.back()
                    lex_table.append((TYPE['<'], ch))
                    continue

            elif ch == '=':
                lex_table.append((TYPE['='], ch))
            elif ch == '>':
                ch = source.get()
                if ch == '=':
                    lex_table.append((TYPE['>='], ch))
                else:
                    source.back()
                    lex_table.append((TYPE['>'], '>'))
                    continue
            elif ch == ':':
                ch = source.get()
                if ch == '=':
                    lex_table.append((TYPE[':='], ':='))
                    continue
                else:
                    print_error(source, 'see : but no =, did you mean := ?')
                    break
            elif ch == ';':
                lex_table.append((TYPE[';'], ch))
                continue
            elif ch == '+':
                lex_table.append((TYPE['+'], ch))
                continue
            elif ch == '-':
                lex_table.append((TYPE['-'], ch))
                continue
            elif ch == '*':
                lex_table.append((TYPE['*'], ch))
                continue
            elif ch == '(':
                lex_table.append((TYPE['('], ch))
                continue
            elif ch == ')':
                lex_table.append((TYPE[')'], ch))
                continue
            elif ch == '/':
                ch = source.get()
                if ch == '*':
                    ch = source.get()
                    while True:
                        if ch == '*':
                            ch = source.get()
                            if ch == '/':
                                break
                        ch = source.get()
                else:
                    source.back()
                    lex_table.append((TYPE['/'], ch))

                continue
            elif ch == '{':
                ch = source.get()
                if ch == '*':
                    while True:
                        if ch == '*':
                            ch = source.get()
                            if ch == '}':
                                break
                        ch = source.get()
                continue

            else:
                print('error at line:%d column%d' % (source.r, source.c))


def print_error(source: Source, msg: str = ''):
    print(msg + (' at row:%d, col:%d' % (source.r, source.c)))
    raise CompileError(msg, (source.r, source.c))


if __name__ == '__main__':
    source = Source('test.pas')
    table = lex(source)
    print(table.table)
