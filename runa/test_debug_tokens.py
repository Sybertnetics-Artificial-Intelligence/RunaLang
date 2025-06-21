#!/usr/bin/env python3
"""
Debug script to test tokenization of Let Be syntax.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from runa.compiler.lexer import RunaLexer

def test_let_be_tokens():
    """Test tokenization of Let Be syntax."""
    source = '''
Let x Be 10
Let y Be 20
Let result Be x plus y
'''
    
    print("Testing Let Be tokenization...")
    print(f"Source: {repr(source)}")
    
    lexer = RunaLexer(source)
    tokens = lexer.tokenize()
    
    print("Tokens:")
    for token in tokens:
        print(f"  {token.type.name}: '{token.value}' (line={token.line}, col={token.column})")

if __name__ == "__main__":
    test_let_be_tokens() 