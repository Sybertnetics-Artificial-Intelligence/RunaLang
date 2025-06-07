"""
Performance Benchmark Tests for Runa Parser.

This module contains benchmark tests to measure parser performance
and ensure it meets performance requirements.
"""

import pytest
import time
import gc
from typing import List

from runa.lexer import RunaLexer
from runa.parser import RunaParser
from runa.errors import ErrorReporter


class TestParserPerformance:
    """Test parser performance benchmarks."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str):
        """Helper to parse code and measure performance."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        return parser.parse()
    
    @pytest.mark.benchmark
    def test_simple_expression_parsing_speed(self, benchmark):
        """Benchmark simple expression parsing speed."""
        code = "5 plus 3 multiplied by 2"
        
        result = benchmark(self.parse_code, code)
        assert result.success
    
    @pytest.mark.benchmark
    def test_complex_expression_parsing_speed(self, benchmark):
        """Benchmark complex expression parsing speed."""
        code = "(5 plus 3) multiplied by (10 minus 2) divided by (8 plus 1)"
        
        result = benchmark(self.parse_code, code)
        assert result.success
    
    @pytest.mark.benchmark
    def test_function_definition_parsing_speed(self, benchmark):
        """Benchmark function definition parsing speed."""
        code = """
        Process calculate_complex(x, y, z) returns number:
            Let result be x plus y
            Set result to result multiplied by z
            Return result
        """
        
        result = benchmark(self.parse_code, code)
        assert result.success
    
    @pytest.mark.benchmark
    def test_large_program_parsing_speed(self, benchmark):
        """Benchmark large program parsing speed."""
        # Generate a moderately large program
        statements = []
        for i in range(50):
            statements.append(f"Let var_{i} be {i}")
            statements.append(f"Set var_{i} to var_{i} plus 1")
        
        code = "\n".join(statements)
        
        result = benchmark(self.parse_code, code)
        assert result.success
    
    def test_parsing_memory_usage(self):
        """Test that parsing doesn't consume excessive memory."""
        # Force garbage collection before test
        gc.collect()
        
        # Generate a large program
        statements = []
        for i in range(100):
            statements.append(f"Let variable_{i} be {i} plus {i+1}")
        
        code = "\n".join(statements)
        
        # Parse the code
        result = self.parse_code(code)
        assert result.success
        
        # Memory usage test would require more sophisticated tooling
        # For now, just ensure parsing completes successfully
        assert result.node is not None
        assert len(result.node.statements) == 100


class TestLexerPerformance:
    """Test lexer performance benchmarks."""
    
    @pytest.mark.benchmark
    def test_tokenization_speed(self, benchmark):
        """Benchmark tokenization speed."""
        code = """
        Define pi as 3.14159
        Let radius be 5
        Let area be pi multiplied by radius multiplied by radius
        Display "Area is:" with area
        """
        
        def tokenize():
            lexer = RunaLexer(code)
            return lexer.tokenize()
        
        result = benchmark(tokenize)
        assert result.success
    
    @pytest.mark.benchmark
    def test_large_file_tokenization(self, benchmark):
        """Benchmark tokenization of large files."""
        # Generate a large code file
        lines = []
        for i in range(200):
            lines.append(f"Let variable_{i} be {i}")
            lines.append(f"Display variable_{i}")
        
        code = "\n".join(lines)
        
        def tokenize():
            lexer = RunaLexer(code)
            return lexer.tokenize()
        
        result = benchmark(tokenize)
        assert result.success
        assert len(result.tokens) > 400  # Should have many tokens 