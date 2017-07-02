from lexer import lex, TYPE
from lextable import LexTable
from compileerror import CompileError


class Parser:
    def __init__(self, table: LexTable):
        self.table = table

    def variable(self):
        """
        V -> ID
        :return:
        """
        if self.table.match(TYPE['ID']):
            self.table.advance()
        else:
            raise CompileError('Expect an identifier, but not found.', self.table.position())

    def integer(self):
        """
        <INT>: number
        :return:
        """
        if self.table.match(TYPE['INT']):
            self.table.advance()
        else:
            raise CompileError("Expect an number, but not found.", self.table.position())

    def relational_operator(self):
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
            self.table.advance()
        else:
            raise CompileError('Expect an relational identifier, but not found.', self.table.position())

    def relational_statement(self):
        """
        RS -> E OP E
        :return:
        """
        self.expression()
        self.relational_operator()
        self.expression()

    def factor(self):
        """
        F -> V | INT | ( E )
        :return:
        """
        if self.table.match(TYPE['(']):
            self.table.advance()
        elif self.table.match(TYPE['INT']):
            self.table.advance()
        else:
            self.variable()

    def term1(self):
        """
        T1 -> * F T1 | / F T1 | EPSILON
        :return:
        """
        if self.table.match(TYPE['*']) or self.table.match(TYPE['/']):
            self.table.advance()
            self.factor()
            self.term1()

    def term(self):
        """
        T -> F T1
        :return:
        """
        self.factor()
        self.term1()

    def expression(self):
        """
        E -> T E1
        :return:
        """
        self.term()
        self.expression1()

    def expression1(self):
        """
        E1 -> + T E1 | - T E1 | EPSILON
        :return:
        """
        if self.table.match(TYPE['+']) or self.table.match(TYPE['-']):
            self.table.advance()
            self.term()
            self.expression1()

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
            self.relational_statement()

            if self.table.match(TYPE['do']):
                self.table.advance()
                self.statement()
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
            self.relational_statement()

            if self.table.match(TYPE['then']):
                self.table.advance()
                self.statement()
            else:
                raise CompileError('Expect "then" but not found.', self.table.position())

            if self.table.match(TYPE['else']):
                self.table.advance()
                self.statement()
        else:
            raise CompileError('Expect "if" but not found.', self.table.position())

    def assignment_statement(self):
        """
        <AS>: <V>:=<E>
        :return:
        """
        self.variable()
        if self.table.match(TYPE[':=']):
            self.table.advance()
            self.expression()

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


if __name__ == '__main__':
    from lexer  import lex
    table = lex('test.pas')
    parser = Parser(table)
    parser.statement_list()