"""
Tests for the Runa compiler integration.
"""

import pytest
from pathlib import Path
import tempfile

from runa.src.compiler import Compiler, CompilationResult


def test_empty_program():
    """Test compiling an empty program."""
    compiler = Compiler()
    result = compiler.compile_string("")
    
    assert result.success
    assert not result.has_errors()
    assert len(result.program.statements) == 0


def test_valid_program():
    """Test compiling a valid program."""
    source = """
    let x = 42;
    let y = x + 10;
    function add(a: Int, b: Int): Int {
        return a + b;
    }
    let result = add(x, y);
    """
    
    compiler = Compiler()
    result = compiler.compile_string(source)
    
    assert result.success
    assert not result.has_errors()
    assert len(result.program.statements) == 4  # 3 declarations and 1 function


def test_lexical_error():
    """Test compilation with lexical errors."""
    source = """
    let x = 42;
    let y = @invalid;  # Invalid character
    """
    
    compiler = Compiler()
    result = compiler.compile_string(source)
    
    assert not result.success
    assert result.has_errors()
    assert len(result.lexer_errors) > 0
    assert len(result.parser_errors) == 0
    assert len(result.semantic_errors) == 0


def test_syntax_error():
    """Test compilation with syntax errors."""
    source = """
    let x = 42;
    let y = ;  # Missing expression
    """
    
    compiler = Compiler()
    result = compiler.compile_string(source)
    
    assert not result.success
    assert result.has_errors()
    assert len(result.lexer_errors) == 0
    assert len(result.parser_errors) > 0
    assert len(result.semantic_errors) == 0


def test_semantic_error():
    """Test compilation with semantic errors."""
    source = """
    let x = 42;
    let y = z;  # Undefined variable
    """
    
    compiler = Compiler()
    result = compiler.compile_string(source)
    
    assert not result.success
    assert result.has_errors()
    assert len(result.lexer_errors) == 0
    assert len(result.parser_errors) == 0
    assert len(result.semantic_errors) > 0


def test_multiple_errors():
    """Test compilation with multiple types of errors."""
    source = """
    let x = 42;
    let y = @invalid;  # Lexical error
    let z = ;          # Syntax error
    let w = undefined; # Semantic error
    """
    
    compiler = Compiler()
    result = compiler.compile_string(source)
    
    assert not result.success
    assert result.has_errors()
    # Since compilation stops at the first stage with errors,
    # we should only see lexical errors here
    assert len(result.lexer_errors) > 0


def test_compile_file():
    """Test compiling from a file."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.runa', delete=False) as temp:
        temp.write(b"let x = 42;\nlet y = x + 10;")
        temp_path = temp.name
    
    try:
        compiler = Compiler()
        result = compiler.compile_file(temp_path)
        
        assert result.success
        assert not result.has_errors()
        assert len(result.program.statements) == 2
    finally:
        # Clean up the temporary file
        Path(temp_path).unlink()


def test_compile_nonexistent_file():
    """Test compiling a nonexistent file."""
    compiler = Compiler()
    result = compiler.compile_file("nonexistent.runa")
    
    assert not result.success
    assert result.has_errors() == False  # No specific errors are recorded, just failure
    assert result.program is None


def test_type_error():
    """Test compilation with type errors."""
    source = """
    let x: Int = "string";  # Type mismatch
    """
    
    compiler = Compiler()
    result = compiler.compile_string(source)
    
    assert not result.success
    assert result.has_errors()
    assert len(result.lexer_errors) == 0
    assert len(result.parser_errors) == 0
    assert len(result.semantic_errors) > 0
    assert "Type mismatch" in str(result.semantic_errors[0])


def test_function_call_errors():
    """Test compilation with function call errors."""
    source = """
    function add(a: Int, b: Int): Int {
        return a + b;
    }
    let result = add(42, "string");  # Type mismatch in argument
    """
    
    compiler = Compiler()
    result = compiler.compile_string(source)
    
    assert not result.success
    assert result.has_errors()
    assert len(result.semantic_errors) > 0 