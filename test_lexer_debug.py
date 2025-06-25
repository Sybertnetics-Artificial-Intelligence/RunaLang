#!/usr/bin/env python3
"""
Debug test to see what tokens the lexer produces for function declarations
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'runa', 'src'))

from runa.compiler.lexer import RunaLexer

def test_function_declaration_tokens():
    """Test what tokens are produced for function declarations."""
    
    # Test the function declaration that's failing
    source = '''Process called "Calculate Area" that takes width and height returns Integer:
    Set area to width multiplied by height
    Return area'''
    
    print("Testing function declaration tokenization:")
    print(f"Source: {repr(source)}")
    print()
    
    lexer = RunaLexer()
    try:
        tokens = lexer.tokenize(source)
        print("Tokens produced:")
        for i, token in enumerate(tokens):
            print(f"  {i:2d}: {token}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50)
    
    # Test a simpler function declaration
    source2 = 'Process called "test" that takes nothing:'
    print(f"Testing simpler function: {repr(source2)}")
    print()
    
    try:
        tokens2 = lexer.tokenize(source2)
        print("Tokens produced:")
        for i, token in enumerate(tokens2):
            print(f"  {i:2d}: {token}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_function_declaration_tokens() 