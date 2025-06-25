#!/usr/bin/env python3
"""
Comprehensive test to verify parser with PROPER RUNA SYNTAX
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'runa', 'src'))

from runa.compiler.lexer import RunaLexer, TokenType
from runa.compiler.parser import RunaParser

def test_basic_expressions():
    """Test basic expression parsing with Runa syntax."""
    test_cases = [
        '"Hello"',           # String literal
        '42',                # Integer literal
        '3.14',              # Float literal
        'true',              # Boolean literal
        'variable_name',     # Identifier
    ]
    
    print("=== Testing Basic Expressions (Universal Syntax) ===")
    for source in test_cases:
        print(f"Testing: {source}")
        
        lexer = RunaLexer()
        tokens = lexer.tokenize(source)
        
        parser = RunaParser()
        parser.set_tokens(tokens)
        try:
            expr = parser.parse_expression()
            print(f"  ✅ Successfully parsed: {type(expr).__name__}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    print()

def test_runa_arithmetic():
    """Test Runa natural language arithmetic expressions."""
    test_cases = [
        '1 plus 2',              # Natural language addition
        '5 minus 3',             # Natural language subtraction 
        'multiply 4 by 6',       # Natural language multiplication (active)
        '4 multiplied by 6',     # Natural language multiplication (passive)
        'divide 8 by 2',         # Natural language division (active)
        '8 divided by 2',        # Natural language division (passive)
        '10 modulo 3',           # Natural language modulo
    ]
    
    print("=== Testing Runa Natural Language Arithmetic ===")
    for source in test_cases:
        print(f"Testing: {source}")
        
        lexer = RunaLexer()
        tokens = lexer.tokenize(source)
        print(f"  Tokens: {[f'{t.type.name}:{t.value}' for t in tokens[:5]]}")  # Show first 5 tokens
        
        parser = RunaParser()
        parser.set_tokens(tokens)
        try:
            expr = parser.parse_expression()
            print(f"  ✅ Successfully parsed: {type(expr).__name__}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    print()

def test_runa_comparisons():
    """Test Runa natural language comparison expressions."""
    test_cases = [
        '5 is greater than 3',       # Natural language comparison
        '2 is less than 7',          # Natural language comparison
        '4 is equal to 4',           # Natural language equality
        'x is not equal to y',       # Natural language inequality
    ]
    
    print("=== Testing Runa Natural Language Comparisons ===")
    for source in test_cases:
        print(f"Testing: {source}")
        
        lexer = RunaLexer()
        tokens = lexer.tokenize(source)
        print(f"  Tokens: {[f'{t.type.name}:{t.value}' for t in tokens[:6]]}")  # Show first 6 tokens
        
        parser = RunaParser()
        parser.set_tokens(tokens)
        try:
            expr = parser.parse_expression()
            print(f"  ✅ Successfully parsed: {type(expr).__name__}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    print()

def test_runa_statements():
    """Test Runa natural language statements."""
    test_cases = [
        'Display "Hello World"',
        'Display 42',
        'let x be 10',               # Natural language variable declaration
        'let name be "Alice"',       # Natural language string variable
    ]
    
    print("=== Testing Runa Natural Language Statements ===")
    for source in test_cases:
        print(f"Testing: {source}")
        
        lexer = RunaLexer()
        tokens = lexer.tokenize(source)
        print(f"  Tokens: {[f'{t.type.name}:{t.value}' for t in tokens[:5]]}")  # Show first 5 tokens
        
        parser = RunaParser()
        try:
            program = parser.parse(tokens)
            print(f"  ✅ Successfully parsed program with {len(program.statements)} statements")
            if program.statements:
                stmt = program.statements[0]
                print(f"    Statement type: {type(stmt).__name__}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    print()

if __name__ == "__main__":
    test_basic_expressions()
    test_runa_arithmetic()
    test_runa_comparisons()
    test_runa_statements() 