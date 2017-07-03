from lexer import lex, TYPE
from lextable import LexTable
from compileerror import CompileError
from typing import *


class Quadruple:
    def __init__(self, op, arg1, arg2, result):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __str__(self):
        arg1 = str(self.arg1) if self.arg1 is not None else 'None'
        arg2 = str(self.arg2) if self.arg2 is not None else 'None'
        return '(' + self.op + ', ' + arg1 + ', ' + arg2 + ', ' + str(self.result) + ')'

    def __getitem__(self, item):
        if item == 0:
            return self.op
        elif item == 1:
            return self.arg1
        elif item == 2:
            return self.arg2
        elif item == 3:
            return self.result


class Label:
    def __init__(self, _id: int):
        self.id = _id


class Parser:
    def __init__(self, lex_table: LexTable):
        self.table = lex_table

        self.e_label: int = 0  # expression label
        self.r_label: int = 0  # relational expression label
        self.t_label: int = 0  # temp label
        self.quadruple: List[Union[Quadruple, Label]] = []

    def new_temp(self) -> str:
        """
        apply for a new temp variable
        :return:
        """
        self.t_label += 1
        return 'T' + str(self.t_label - 1)

    def new_label(self) -> None:
        """
        append a new label to the list
        :return:
        """
        self.quadruple.append(Label(self.t_label))
        self.t_label += 1

    def variable(self) -> str:
        """
        V -> ID
        :return:
        """
        if self.table.match(TYPE['ID']):
            text = self.table.get()
            self.table.advance()
            return text
        else:
            raise CompileError('Expect an identifier, but not found.', self.table.position())

    def integer(self) -> int:
        """
        <INT>: number
        :return:
        """
        if self.table.match(TYPE['INT']):
            text = self.table.get()
            self.table.advance()
            return text
        else:
            raise CompileError("Expect an number, but not found.", self.table.position())

    def relational_operator(self) -> str:
        """
        OP -> < | <= | == | > | >= | <>
        :return:
        """
        if self.table.match(TYPE['>']) or \
                self.table.match(TYPE['>=']) or \
                self.table.match(TYPE['<']) or \
                self.table.match(TYPE['<=']) or \
                self.table.match(TYPE['=']) or \
                self.table.match(TYPE['<>']):
            text = self.table.get()
            self.table.advance()
            return text.content
        else:
            raise CompileError('Expect an relational identifier, but not found.', self.table.position())

    def relational_statement(self):
        """
        RS -> E OP E
        :return:
        """
        arg1 = self.expression()
        op = self.relational_operator()
        arg2 = self.expression()
        result = self.new_temp()
        self.quadruple.append(Quadruple(op, arg1, arg2, result))
        return result

    def factor(self):
        """
        F -> V | INT | ( E )
        :return:
        """
        if self.table.match(TYPE['(']):
            self.table.advance()
            text = self.expression()
            if self.table.match(TYPE[')']):
                return text
            else:
                raise CompileError('Missing parenthesis.', self.table.position())
        elif self.table.match(TYPE['INT']):
            text = self.table.get()
            self.table.advance()
            return text
        else:
            text = self.variable()
            return text

    # def term1(self):
    #     """
    #     T1 -> * F T1 | / F T1 | EPSILON
    #     :return:
    #     """
    #     if self.table.match(TYPE['*']) or self.table.match(TYPE['/']):
    #         self.table.advance()
    #         self.factor()
    #         self.term1()

    def term(self):
        """
        T -> F T1
        T -> F { [*/] F }
        :return:
        """
        arg1 = self.factor()
        # self.term1()

        while self.table.match(TYPE['*']) or self.table.match(TYPE['/']):
            op = self.table.get()
            self.table.advance()
            arg2 = self.factor()
            result = self.new_temp()
            self.quadruple.append(Quadruple(op.content, arg1, arg2, result))
            arg1 = result

        return arg1

    def expression(self):
        """
        E -> T E1
        :return:
        """
        arg1 = self.term()
        # self.expression1()

        while self.table.match(TYPE['+']) or self.table.match(TYPE['-']):
            text = self.table.get()
            self.table.advance()
            arg2 = self.term()
            result = self.new_temp()
            self.quadruple.append(Quadruple(text.content, arg1, arg2, result))
            arg1 = result

        return arg1

    # def expression1(self):
    #     """
    #     E1 -> + T E1 | - T E1 | EPSILON
    #     :return:
    #     """
    #     if self.table.match(TYPE['+']) or self.table.match(TYPE['-']):
    #         self.table.advance()
    #         self.term()
    #         self.expression1()

    def multiple_statement(self):
        """
        MS -> begin SL end
        :return:
        """
        if self.table.match(TYPE['begin']):
            self.table.advance()
            self.statement_list()
            if self.table.match(TYPE['end']):
                self.table.advance()
            else:
                raise CompileError('Expect "end" but not found.', self.table.position())
        else:
            raise CompileError('Expect "begin" but not found.', self.table.position())

    def while_statement(self):
        """
        WHILE -> while RS do S
        :return:
        """
        if self.table.match(TYPE['while']):
            self.table.advance()
            begin = len(self.quadruple)
            arg1 = self.relational_statement()

            if self.table.match(TYPE['do']):
                tc = len(self.quadruple)  # true chain
                self.quadruple.append(Quadruple('jnz', arg1, None, 0))
                fc = len(self.quadruple)  # false chain
                self.quadruple.append(Quadruple('jmp', None, None, 0))

                self.table.advance()
                self.quadruple[tc].result = len(self.quadruple)  # backpatch true chain
                self.statement()
                self.quadruple[fc].result = len(self.quadruple)  # behind statement is false chain, backpatch it
            else:
                raise CompileError('Expect "do" but not found.', self.table.position())
        else:
            raise CompileError('Expect "while" but not found.', self.table.position())

    def conditional_statement(self):
        """
        CS -> if RS then S else S
        :return:
        """
        if self.table.match(TYPE['if']):
            self.table.advance()
            arg1 = self.relational_statement()

            tc = len(self.quadruple)  # true chain
            self.quadruple.append(Quadruple('jnz', arg1, None, 0))
            fc = len(self.quadruple)  # false chain
            self.quadruple.append(Quadruple('jmp', None, None, 0))

            if self.table.match(TYPE['then']):
                self.table.advance()
                # self.new_label()
                self.quadruple[tc].result = len(self.quadruple)  # backpatch true chain
                self.statement()
            else:
                raise CompileError('Expect "then" but not found.', self.table.position())

            if self.table.match(TYPE['else']):
                self.table.advance()
                self.quadruple[fc].result = len(self.quadruple)  # backpatch false chain
                self.statement()
        else:
            raise CompileError('Expect "if" but not found.', self.table.position())

    def assignment_statement(self):
        """
        <AS>: <V>:=<E>
        :return:
        """
        arg1 = self.variable()
        if self.table.match(TYPE[':=']):
            self.table.advance()
            arg2 = self.expression()
            result = self.new_temp()
            self.quadruple.append(Quadruple(':=', arg1, arg2, result))

    def statement(self):
        """
        S -> AS | CS | WHILE | MS
        :return:
        """
        if self.table.look_forward(TYPE['ID']):
            self.assignment_statement()
        elif self.table.look_forward(TYPE['if']):
            self.conditional_statement()
        elif self.table.look_forward(TYPE['while']):
            self.while_statement()
        elif self.table.look_forward(TYPE['begin']):
            self.multiple_statement()

    def statement_list(self):
        """
        SL -> S SL1
        :return:
        """
        self.statement()
        self.statement_list1()

    def statement_list1(self):
        """
        SL1 -> ; SL | EPSILON
        :return:
        """
        if self.table.match(TYPE[';']):
            self.table.advance()
            self.statement_list()

    def parse(self):
        self.statement_list()


if __name__ == '__main__':
    from lexer import lex
    from source import Source

    source = Source('test.pas')
    table = lex(source)
    parser = Parser(table)
    parser.parse()

    for i in range(len(parser.quadruple)):
        print('{0}:\t{1}'.format(i, str(parser.quadruple[i])))
