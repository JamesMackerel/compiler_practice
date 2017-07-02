from typing import *


class Node:
    def __init__(self, node_type: str, content: str):
        self.type = node_type
        self.content = content


class ProductorBody:
    def __init__(self, *args: str):
        self.body = []  # type:List[Node]

        for node in args:
            if node.startswith('<'):  # a non-terminate
                self.body.append(Node('n', node))
            else:
                self.body.append(Node('t', node))

    def __iter__(self):
        return iter(self.body)

    def __str__(self):
        r = ''
        for node in self.body:
            r += node.content

        return r


class Productor:
    def __init__(self):
        self.productor = {}  # type: Dict[str, List[ProductorBody]]
        self.productor = {
            '<SL>': [
                ProductorBody('<S>'),
                ProductorBody('<S>', ';', '<SL>'),
            ],
            '<S>': [
                ProductorBody('<AS>'),
                ProductorBody('<CS>'),
                ProductorBody('<WHILE>'),
                ProductorBody('<MS>'),
            ],
            '<AS>': [
                ProductorBody('<V>',":=",'<E>'),
            ],
            '<CS>': [
                ProductorBody('if', '<RS>', 'then', '<S>', 'else', '<S>'),
            ],
            '<WHILE>': [
                ProductorBody('while', '<RS>', 'do', '<S>'),
            ],
            '<MS>': [
                ProductorBody('begin', '<RS>', 'do', '<S>'),
            ],
            '<E>': [
                ProductorBody('<T>'),
                ProductorBody('<E>', '+', '<T>'),
                ProductorBody('<E>', '-', '<T>'),
            ],
            '<T>': [
                ProductorBody('<F>'),
                ProductorBody('<T>', '*', '<F>'),
                ProductorBody('<T>', '/', '<F>'),
            ],
            '<F>': [
                ProductorBody('<V>'),
                ProductorBody('INT'),
                ProductorBody('(', '<E>', ')'),
            ],
            '<RS>': [
                ProductorBody('<E>', '<OP>', '<E>'),
            ],
            '<V>': [
                ProductorBody('ID'),
            ],
            '<OP>': [
                ProductorBody('<'),
                ProductorBody('<='),
                ProductorBody('<>'),
                ProductorBody('>'),
                ProductorBody('>='),
                ProductorBody('='),
            ]
        }

        self.first = {}  # type:Dict[str, List[str]]
        self.follow = {}  # type:Dict[str, List[str]]

    def caculate_first(self):
        """
        caculate non-terminate's first set.
        :return:
        """

    def load(self, file_path: str):
        """
        load productor from file
        :param file_path: path to the productor file
        :return:
        """
        pass

    def __str__(self):
        r = ''
        for head, body in self.productor.items():
            r += head
            r += ' -> '
            for b in body[:len(body)-1]:
                r += str(b)
                r += ' | '
            r += str(body[len(body)-1])
            r += '\n'

        return r


if __name__ == "__main__":
    p = Productor()
    print (p)
