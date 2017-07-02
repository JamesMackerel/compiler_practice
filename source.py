from typing import *


class Source:
    """
    represents a source file.
    load all content to memory when initialize the object.
    """

    def __init__(self, file: str) -> None:
        with open(file) as f:
            self.source = f.read()

        self.source += '\n'

        self.i = 0  # index
        self.r = 0  # row
        self.c = 0  # column
        self.columns = []  # type: List[int]

    def get(self) -> Optional[str]:
        """
        get next character
        :return: next character if exists, else returns None
        """
        try:
            ch = self.source[self.i]
        except IndexError:
            return None

        self.i += 1
        self.c += 1

        if ch == '\n':
            self.columns.append(self.c)
            self.r += 1
            self.c = 0

        return ch

    def back(self) -> None:
        self.i -= 1
        if self.c == 0: # at the start of line
            self.r -= 1
            self.c = self.columns.pop()
        else:
            self.c -= 1

    def current_position(self) -> Tuple[int, int]:
        """
        get current position
        :return: (row, column)
        """
        return self.r + 1, self.c
