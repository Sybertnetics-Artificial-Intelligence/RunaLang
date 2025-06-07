"""
Comprehensive Semantic Analyzer Tests for Runa Programming Language.

This module contains extensive tests for the semantic analyzer,
covering all analysis passes, error detection, and validation.

Test Categories:
- Symbol collection and scoping
- Type checking and validation
- Usage analysis
- Error detection and reporting
- Multi-pass analysis
- AI/ML specific constructs
"""

import pytest
from unittest.mock import Mock
from typing import List, Any

from runa.lexer import RunaLexer
from runa.parser import RunaParser
from runa.semantic_analyzer import SemanticAnalyzer, AnalysisResult, AnalysisPass
from runa.symbol_table import SymbolTable, Symbol, SymbolType
from runa.ast_nodes import *
from runa.errors import SourcePosition, RunaSemanticError, ErrorReporter


class TestSemanticAnalyzerBasics:
    """Test basic semantic analyzer functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
        self.analyzer = SemanticAnalyzer(self.error_reporter)
    
    def parse_and_analyze(self, code: str) -> AnalysisResult:
        """Helper to parse and analyze code string."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        parse_result = parser.parse()
        
        if not parse_result.success:
            pytest.fail(f"Parser failed: {parse_result.errors}")
        
        return self.analyzer.analyze(parse_result.node)
    
    def test_empty_program(self):
        """Test analyzing an empty program."""
        result = self.parse_and_analyze("")
        
        assert result.success
        assert len(result.errors) == 0
        assert len(result.warnings) == 0
        assert result.symbol_table is not None
    
    def test_simple_declaration(self):
        """Test analyzing a simple variable declaration."""
        result = self.parse_and_analyze("Let x be 5")
        
        assert result.success
        assert len(result.errors) == 0
        
        # Check symbol was created
        symbol = result.symbol_table.lookup("x")
        assert symbol is not None
        assert symbol.name == "x"
        assert symbol.symbol_type == SymbolType.VARIABLE
        assert symbol.is_mutable
        assert symbol.is_initialized
    
    def test_constant_declaration(self):
        """Test analyzing a constant declaration."""
        result = self.parse_and_analyze('Define pi as 3.14159')
        
        assert result.success
        assert len(result.errors) == 0
        
        # Check symbol was created
        symbol = result.symbol_table.lookup("pi")
        assert symbol is not None
        assert symbol.name == "pi"
        assert symbol.symbol_type == SymbolType.CONSTANT
        assert not symbol.is_mutable
        assert symbol.is_initialized


class TestSymbolCollection:
    """Test symbol collection pass."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
        self.analyzer = SemanticAnalyzer(self.error_reporter)
    
    def parse_and_analyze(self, code: str) -> AnalysisResult:
        """Helper to parse and analyze code string."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens.tokens, self.error_reporter)
        parse_result = parser.parse()
        return self.analyzer.analyze(parse_result.node)
    
    def test_variable_redefinition_error(self):
        """Test error on variable redefinition."""
        code = """
        Let x be 5
        Let x be 10
        """
        result = self.parse_and_analyze(code)
        
        assert not result.success
        assert len(result.errors) >= 1
        assert any("Redefinition" in error.message for error in result.errors)
    
    def test_function_definition(self):
        """Test function definition symbol collection."""
        code = """
        Process calculate(x, y) returns number:
            Return x plus y
        """
        result = self.parse_and_analyze(code)
        
        assert result.success
        
        # Check function symbol
        func_symbol = result.symbol_table.lookup("calculate")
        assert func_symbol is not None
        assert func_symbol.symbol_type == SymbolType.FUNCTION
        assert len(func_symbol.parameters) == 2
    
    def test_nested_scoping(self):
        """Test nested scope handling."""
        code = """
        Let x be 5
        Process test():
            Let x be 10
            Display x
        """
        result = self.parse_and_analyze(code)
        
        assert result.success
        # Should not have redefinition error due to different scopes
        assert len(result.errors) == 0
    
    def test_undefined_variable_error(self):
        """Test error on undefined variable usage."""
        code = "Set undefined_var to 42"
        result = self.parse_and_analyze(code)
        
        assert not result.success
        assert len(result.errors) >= 1
        assert any("undeclared" in error.message.lower() for error in result.errors)


class TestTypeChecking:
    """Test type checking pass."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
        self.analyzer = SemanticAnalyzer(self.error_reporter)
    
    def parse_and_analyze(self, code: str) -> AnalysisResult:
        """Helper to parse and analyze code string."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens.tokens, self.error_reporter)
        parse_result = parser.parse()
        return self.analyzer.analyze(parse_result.node)
    
    def test_type_annotation_validation(self):
        """Test type annotation validation."""
        code = 'Let x (unknown_type) be 5'
        result = self.parse_and_analyze(code)
        
        # Should have warning about unknown type
        assert len(result.warnings) >= 1
        assert any("Unknown type" in warning.message for warning in result.warnings)
    
    def test_type_mismatch_warning(self):
        """Test type mismatch detection."""
        code = 'Let x (string) be 42'
        result = self.parse_and_analyze(code)
        
        # Should have warning about type mismatch
        assert len(result.warnings) >= 1
        assert any("Type mismatch" in warning.message for warning in result.warnings)
    
    def test_constant_assignment_error(self):
        """Test error on constant assignment."""
        code = """
        Define pi as 3.14159
        Set pi to 3.14
        """
        result = self.parse_and_analyze(code)
        
        assert not result.success
        assert len(result.errors) >= 1
        assert any("constant" in error.message.lower() for error in result.errors)
    
    def test_division_by_zero_warning(self):
        """Test division by zero warning."""
        code = "Let result be 10 divided by 0"
        result = self.parse_and_analyze(code)
        
        # Should have warning about division by zero
        assert len(result.warnings) >= 1
        assert any("Division by zero" in warning.message for warning in result.warnings)


class TestUsageAnalysis:
    """Test usage analysis pass."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
        self.analyzer = SemanticAnalyzer(self.error_reporter)
    
    def parse_and_analyze(self, code: str) -> AnalysisResult:
        """Helper to parse and analyze code string."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens.tokens, self.error_reporter)
        parse_result = parser.parse()
        return self.analyzer.analyze(parse_result.node)
    
    def test_unused_variable_warning(self):
        """Test warning for unused variables."""
        code = """
        Let unused_var be 42
        Let used_var be 10
        Display used_var
        """
        result = self.parse_and_analyze(code)
        
        # Should have warning about unused variable
        assert len(result.warnings) >= 1
        assert any("never used" in warning.message for warning in result.warnings)
    
    def test_variable_usage_tracking(self):
        """Test proper variable usage tracking."""
        code = """
        Let x be 5
        Let y be x plus 10
        Display y
        """
        result = self.parse_and_analyze(code)
        
        # Should not have unused variable warnings
        unused_warnings = [w for w in result.warnings if "never used" in w.message]
        assert len(unused_warnings) == 0


class TestControlFlow:
    """Test control flow analysis."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
        self.analyzer = SemanticAnalyzer(self.error_reporter)
    
    def parse_and_analyze(self, code: str) -> AnalysisResult:
        """Helper to parse and analyze code string."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens.tokens, self.error_reporter)
        parse_result = parser.parse()
        return self.analyzer.analyze(parse_result.node)
    
    def test_break_outside_loop_error(self):
        """Test error for break statement outside loop."""
        code = """
        Let x be 5
        Break
        """
        result = self.parse_and_analyze(code)
        
        assert not result.success
        assert len(result.errors) >= 1
        assert any("Break statement outside loop" in error.message for error in result.errors)
    
    def test_continue_outside_loop_error(self):
        """Test error for continue statement outside loop."""
        code = """
        Let x be 5
        Continue
        """
        result = self.parse_and_analyze(code)
        
        assert not result.success
        assert len(result.errors) >= 1
        assert any("Continue statement outside loop" in error.message for error in result.errors)
    
    def test_break_in_loop_valid(self):
        """Test valid break statement in loop."""
        code = """
        While true:
            Break
        """
        result = self.parse_and_analyze(code)
        
        # Should not have break-related errors
        break_errors = [e for e in result.errors if "Break statement" in e.message]
        assert len(break_errors) == 0
    
    def test_return_outside_function_error(self):
        """Test error for return statement outside function."""
        code = """
        Let x be 5
        Return x
        """
        result = self.parse_and_analyze(code)
        
        assert not result.success
        assert len(result.errors) >= 1
        assert any("Return statement outside function" in error.message for error in result.errors)


class TestFunctionAnalysis:
    """Test function-specific analysis."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
        self.analyzer = SemanticAnalyzer(self.error_reporter)
    
    def parse_and_analyze(self, code: str) -> AnalysisResult:
        """Helper to parse and analyze code string."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens.tokens, self.error_reporter)
        parse_result = parser.parse()
        return self.analyzer.analyze(parse_result.node)
    
    def test_function_redefinition_error(self):
        """Test error on function redefinition."""
        code = """
        Process test():
            Display "First"
        
        Process test():
            Display "Second"
        """
        result = self.parse_and_analyze(code)
        
        assert not result.success
        assert len(result.errors) >= 1
        assert any("Redefinition" in error.message for error in result.errors)
    
    def test_undefined_function_call_error(self):
        """Test error on undefined function call."""
        code = 'Call undefined_function()'
        result = self.parse_and_analyze(code)
        
        assert not result.success
        assert len(result.errors) >= 1
        assert any("Undefined function" in error.message for error in result.errors)
    
    def test_missing_return_warning(self):
        """Test warning for function with return type but no return statement."""
        code = """
        Process calculate() returns number:
            Let x be 5
        """
        result = self.parse_and_analyze(code)
        
        # Should have warning about missing return
        assert len(result.warnings) >= 1
        assert any("no return statement" in warning.message for warning in result.warnings)


class TestAIMLConstructs:
    """Test AI/ML specific construct analysis."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
        self.analyzer = SemanticAnalyzer(self.error_reporter)
    
    def parse_and_analyze(self, code: str) -> AnalysisResult:
        """Helper to parse and analyze code string."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens.tokens, self.error_reporter)
        parse_result = parser.parse()
        return self.analyzer.analyze(parse_result.node)
    
    def test_model_definition_analysis(self):
        """Test model definition analysis."""
        code = """
        Model classifier:
            Architecture: sequential
            Layers: dense(128), dropout(0.2), dense(10)
        """
        result = self.parse_and_analyze(code)
        
        # Should create model symbol
        model_symbol = result.symbol_table.lookup("classifier")
        assert model_symbol is not None
        assert model_symbol.symbol_type == SymbolType.CLASS
    
    def test_unknown_layer_type_warning(self):
        """Test warning for unknown layer types."""
        code = """
        Layer unknown_layer:
            Type: unknown_type
            Config: {}
        """
        result = self.parse_and_analyze(code)
        
        # Should have warning about unknown layer type
        assert len(result.warnings) >= 1
        assert any("Unknown layer type" in warning.message for warning in result.warnings)


class TestErrorRecovery:
    """Test error recovery and reporting."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
        self.analyzer = SemanticAnalyzer(self.error_reporter)
    
    def parse_and_analyze(self, code: str) -> AnalysisResult:
        """Helper to parse and analyze code string."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens.tokens, self.error_reporter)
        parse_result = parser.parse()
        return self.analyzer.analyze(parse_result.node)
    
    def test_multiple_errors_reported(self):
        """Test that multiple errors are properly reported."""
        code = """
        Let x be undefined_var
        Set undefined_var2 to 42
        Define pi as 3.14
        Set pi to 3.15
        """
        result = self.parse_and_analyze(code)
        
        assert not result.success
        # Should have multiple errors
        assert len(result.errors) >= 2
    
    def test_error_positions(self):
        """Test that errors have proper source positions."""
        code = """
        Let x be 5
        Set undefined_var to 42
        """
        result = self.parse_and_analyze(code)
        
        assert not result.success
        assert len(result.errors) >= 1
        
        # Check that error has position information
        error = result.errors[0]
        assert error.position is not None
        assert error.position.line > 0
        assert error.position.column > 0


class TestComplexPrograms:
    """Test analysis of complex programs."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
        self.analyzer = SemanticAnalyzer(self.error_reporter)
    
    def parse_and_analyze(self, code: str) -> AnalysisResult:
        """Helper to parse and analyze code string."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens.tokens, self.error_reporter)
        parse_result = parser.parse()
        return self.analyzer.analyze(parse_result.node)
    
    def test_comprehensive_program(self):
        """Test analysis of a comprehensive program."""
        code = """
        # Define constants
        Define max_iterations as 100
        Define learning_rate as 0.01
        
        # Declare variables
        Let current_iteration be 0
        Let loss be 1.0
        
        # Define function
        Process train_model(data, labels) returns number:
            Let epoch be 0
            While epoch is less than max_iterations:
                # Training logic here
                Set loss to loss multiplied by 0.99
                Set epoch to epoch plus 1
            Return loss
        
        # Main execution
        Let training_data be list containing 1, 2, 3
        Let labels be list containing 0, 1, 0
        Let final_loss be train_model(training_data, labels)
        Display "Training completed with loss:" with final_loss
        """
        result = self.parse_and_analyze(code)
        
        assert result.success
        assert len(result.errors) == 0
        
        # Check that all symbols were created
        assert result.symbol_table.lookup("max_iterations") is not None
        assert result.symbol_table.lookup("learning_rate") is not None
        assert result.symbol_table.lookup("current_iteration") is not None
        assert result.symbol_table.lookup("train_model") is not None
        assert result.symbol_table.lookup("final_loss") is not None
    
    def test_nested_scopes_complex(self):
        """Test complex nested scope scenarios."""
        code = """
        Let global_var be "global"
        
        Process outer_function():
            Let outer_var be "outer"
            
            Process inner_function():
                Let inner_var be "inner"
                Display global_var
                Display outer_var
                Display inner_var
            
            Call inner_function()
            Display outer_var
        
        Call outer_function()
        Display global_var
        """
        result = self.parse_and_analyze(code)
        
        assert result.success
        # Should handle nested scopes correctly without errors
        assert len(result.errors) == 0 