from typing import *
from source import Source


class Lexeme:
    def __init__(self, lex_type:int, lex_content:Union[int, str], lex_position:Tuple[int, int]):
        self.type = lex_type
        self.content = lex_content
        self.position = lex_position

    def __repr__(self):
        return '({0}, {1}, ({2}, {3}))'.format(self.type, self.content, self.position[0], self.position[1])

    def __str__(self):
        return '({0}, {1}, ({2}, {3}))'.format(self.type, self.content, self.position[0], self.position[1])


class LexTable:
    def __init__(self, source: Source):
        self.table = []  # type:List[Lexeme]
        self.i = 0  # type:int
        self.source = source

    def get(self):
        try:
            word = self.table[self.i]
            self.i += 1
            return word
        except IndexError:
            self.i = 0
            return None

    def advance(self):
        self.i += 1

    def match(self, lex_type: int) -> Optional[bool]:
        try:
            return self.table[self.i][0] == lex_type
        except IndexError:
            return None

    def append(self, lex: Tuple[int, Union[str, int]]):
        """
        append lex to table
        :param lex: (type, content)
        """
        lexeme = Lexeme(lex[0], lex[1], self.source.current_position())
        self.table.append(lexeme)
