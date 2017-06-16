from typing import *
from lextable import LexTable
from source import Source

# all key words are in lower case, operators are in upper case
TYPE = {
    'begin': 1,
    'end': 2,
    'if': 3,
    'then': 4,
    'else': 5,
    'ID': 6,
    'INT': 7,
    'LT': 8,
    'LE': 9,
    'EQ': 10,
    'NE': 11,
    'GT': 12,
    'GE': 13,
    'PLUS': 14,
    'DEC': 15,
    'MUL': 16,
    'DIV': 17,
    'MOV': 18,
    'var': 19,
    'while': 20,
    'program': 21,
    'procedure': 22,
    'do': 23,
    'EOS': 24,  # End Of Sentence
    'integer': 25,
    'function': 26,
    'LP': 27,  # (
    'RP': 28  # )
}



def lex(source_path: str) -> LexTable:
    """
    :param source_path: path to the source code file
    :return: List of tuple, which stores key word and identifiers and its type
    """
    source = Source(source_path)
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
                    lex_table.append((TYPE['LE'], ch))
                elif ch == '>':
                    lex_table.append((TYPE['NE'], ch))
                else:
                    source.back()
                    lex_table.append((TYPE['LT'], ch))
                    continue

            elif ch == '=':
                lex_table.append((TYPE['EQ'], ch))
            elif ch == '>':
                ch = source.get()
                if ch == '=':
                    lex_table.append((TYPE['GE'], ch))
                else:
                    source.back()
                    lex_table.append((TYPE['GT'], ch))
                    continue
            elif ch == ':':
                ch = source.get()
                if ch == '=':
                    lex_table.append((TYPE['MOV'], ch))
                    continue
                else:
                    print_error(source, 'see : but no =, did you mean := ?')
                    break
            elif ch == ';':
                lex_table.append((TYPE['EOS'], ch))
                continue
            elif ch == '+':
                lex_table.append((TYPE['PLUS'], ch))
                continue
            elif ch == '-':
                lex_table.append((TYPE['DEC'], ch))
                continue
            elif ch == '*':
                lex_table.append((TYPE['MUL'], ch))
                continue
            elif ch == '(':
                lex_table.append((TYPE['LP'], ch))
                continue
            elif ch == ')':
                lex_table.append((TYPE['RP'], ch))
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
                    lex_table.append((TYPE['DIV'], ch))

                continue

            else:
                print('error at line:%d column%d' % (source.r, source.c))


def print_error(source: Source, msg: str = ''):
    print(msg + (' at row:%d, col:%d' % (source.r, source.c)))


if __name__ == '__main__':
    table = lex('test.pas')
    print(table.table)
