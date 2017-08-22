本项目为编译原理课程设计

# 项目简介
输入语言为PASCAL

词法分析直接用了一个课本上给出的状态机，用if-elif实现。

使用递归下降的语法分析。没有生成AST，直接在语法分析的时候进行语义分析。

图形界面基于PyQt5

# 如何运行
使用 Python 3.6 运行项目根目录下的 run.py 即可，请在运行前安装 PyQt5 

--------

This is a course exercice for Compiler Theory.

# Introduce
Accept a subset of PASCAL as input language.

Lexer uses a state machine given in the text book, implemented in "if-else".

Parse with RECURSIVE DOWN method, and AST is generated, SYMANTIC ANALYSIS is done while parsing.

GUI is PyQt5 based.

# How to run
Run "run.py" in the root directory of this project in Python 3.6. Please install PyQt5 before running.
