#!/usr/bin/env python3

from src.runa.compiler.lexer import RunaLexer
from src.runa.compiler.parser import RunaParser

def test_control_flow():
    lexer = RunaLexer()
    source = """if x is greater than 0:
    Display "Positive"
otherwise:
    Display "Negative"
"""
    tokens = lexer.tokenize(source)
    
    print("Tokens generated:")
    for i, token in enumerate(tokens):
        print(f"  {i}: {token.type.name} = '{token.value}'")
    
    print("\nParsing...")
    parser = RunaParser()
    try:
        ast = parser.parse(tokens)
        print(f"AST type: {type(ast)}")
        print(f"Number of statements: {len(ast.statements)}")
        if ast.statements:
            print(f"First statement type: {type(ast.statements[0])}")
            print(f"First statement: {ast.statements[0]}")
    except Exception as e:
        print(f"Parsing error: {e}")

if __name__ == "__main__":
    test_control_flow() 