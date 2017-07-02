from typing import *


class CompileError(Exception):
    def __init__(self, message: str, position: Tuple[int, int]):
        super().__init__(message, position)
        self.message = message
        self.position = position

    def __repr__(self):
        return '"{0}" at {1}:{2}'.format(self.message, self.position[0], self.position[1])

    def __str__(self):
        return '"{0}" at {1}:{2}'.format(self.message, self.position[0], self.position[1])

if __name__ == '__main__':
    try:
        raise CompileError('expect a integer number, but not found.', (1, 22))
    except CompileError as e:
        print(e)

