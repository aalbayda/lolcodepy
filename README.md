# LOLCODE - Python Interpreter

Submitted in fulfillment of my final project for CMSC124 (*Design and Implementation of Programming Languages*), University of the Philippines Los Baños. The goal was to build an [interpreter](https://en.wikipedia.org/wiki/Interpreter_(computing)) the [LOLCODE](https://en.wikipedia.org/wiki/LOLCODE) programming language from the ground up.

The interpreter goes through three stages:

1. Lexical Analysis (lexer.py) - captures [tokens](https://en.wikipedia.org/wiki/Lexical_analysis) defined in LOLCODE
2. Syntax Analysis (parser.py) - enforces grammar with a [parse tree](https://en.wikipedia.org/wiki/Parse_tree)
3. Semantic Analysis (interpreter.py) - executes source code with a [symbol table](https://en.wikipedia.org/wiki/Symbol_table)

A PyQt UI displays all lexemes and symbols as the LOLCODE source is executed.
The code has been largely obfuscated to avoid issues with university policy. 

# Demo



https://github.com/aalbayda/lolcodepy/assets/33396782/a68da128-ff90-4daf-add1-798f037dbb7b



# Set Up

To run, follow these steps:

1. Install python3: https://www.python.org/downloads/
2. Run `pip3 install PyQt5` on your terminal to install the PyQt library
3. Run `python3 main.py`
