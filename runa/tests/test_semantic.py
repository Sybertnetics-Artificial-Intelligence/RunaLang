"""
Tests for the semantic analyzer of the Runa programming language.
"""

import pytest

from runa.src.lexer.lexer import Lexer
from runa.src.parser.parser import Parser
from runa.src.semantic.analyzer import SemanticAnalyzer, SemanticError
from runa.src.semantic.symboltable import SymbolTable, Symbol, SymbolType


def analyze_code(code: str):
    """
    Helper function to analyze a code snippet.
    
    Args:
        code: The code to analyze
        
    Returns:
        Tuple of (program, errors)
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    program = parser.parse()
    
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(program)
    
    return program, errors


def test_valid_declaration():
    """Test a valid variable declaration."""
    code = """
    let x = 42;
    """
    program, errors = analyze_code(code)
    
    assert len(errors) == 0


def test_duplicate_variable():
    """Test detection of duplicate variable declaration."""
    code = """
    let x = 42;
    let x = 100;  // Error: Duplicate variable
    """
    program, errors = analyze_code(code)
    
    assert len(errors) > 0
    assert "already defined" in errors[0].message


def test_undefined_variable():
    """Test detection of undefined variable usage."""
    code = """
    let y = x + 5;  // Error: Undefined variable x
    """
    program, errors = analyze_code(code)
    
    assert len(errors) > 0
    assert "Undefined variable" in errors[0].message


def test_type_mismatch():
    """Test detection of type mismatch in variable assignment."""
    code = """
    let x: Int = "hello";  // Error: Type mismatch
    """
    program, errors = analyze_code(code)
    
    assert len(errors) > 0
    assert "Type mismatch" in errors[0].message


def test_valid_function():
    """Test a valid function definition and call."""
    code = """
    function add(a: Int, b: Int): Int {
        return a + b;
    }
    
    let result = add(5, 10);
    """
    program, errors = analyze_code(code)
    
    assert len(errors) == 0


def test_function_wrong_arg_count():
    """Test detection of wrong argument count in function call."""
    code = """
    function add(a: Int, b: Int): Int {
        return a + b;
    }
    
    let result = add(5);  // Error: Wrong number of arguments
    """
    program, errors = analyze_code(code)
    
    assert len(errors) > 0
    assert "expects" in errors[0].message


def test_function_return_type_mismatch():
    """Test detection of return type mismatch in function."""
    code = """
    function add(a: Int, b: Int): Int {
        return "result";  // Error: Return type mismatch
    }
    """
    program, errors = analyze_code(code)
    
    assert len(errors) > 0
    assert "Type mismatch" in errors[0].message


def test_boolean_condition():
    """Test that conditions must be boolean."""
    code = """
    if (42) {  // Error: Condition must be boolean
        let x = 10;
    }
    """
    program, errors = analyze_code(code)
    
    assert len(errors) > 0
    assert "Boolean" in errors[0].message


def test_arithmetic_operators():
    """Test type checking of arithmetic operators."""
    code = """
    let a = 5 + 10;       // Valid
    let b = 5.0 + 10;     // Valid, result is Float
    let c = "hello" + 5;  // Error: Invalid operands
    """
    program, errors = analyze_code(code)
    
    assert len(errors) > 0
    assert "Invalid operands" in errors[0].message


def test_loop_variable_scope():
    """Test that loop variables are properly scoped."""
    code = """
    for item in [1, 2, 3] {
        let x = item + 1;
    }
    
    let y = item;  // Error: item is not defined outside loop
    """
    program, errors = analyze_code(code)
    
    assert len(errors) > 0
    assert "Undefined variable" in errors[0].message 