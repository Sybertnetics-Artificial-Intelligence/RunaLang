"""
End-to-End Integration Tests for Runa Programming Language.

This module contains integration tests that verify the complete
pipeline from lexing through parsing to semantic analysis.
"""

import pytest
from typing import List, Any

from runa.lexer import RunaLexer
from runa.parser import RunaParser
from runa.semantic_analyzer import SemanticAnalyzer
from runa.ast_visualizer import ASTTextVisualizer
from runa.errors import ErrorReporter


class TestCompleteLanguagePipeline:
    """Test the complete language processing pipeline."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def process_code(self, code: str):
        """Process code through the complete pipeline."""
        # Step 1: Lexical analysis
        lexer = RunaLexer(code)
        token_result = lexer.tokenize()
        
        if not token_result.success:
            return {"stage": "lexer", "success": False, "errors": token_result.errors}
        
        # Step 2: Parsing
        parser = RunaParser(token_result.tokens, self.error_reporter)
        parse_result = parser.parse()
        
        if not parse_result.success:
            return {"stage": "parser", "success": False, "errors": parse_result.errors}
        
        # Step 3: Semantic analysis
        analyzer = SemanticAnalyzer(self.error_reporter)
        analysis_result = analyzer.analyze(parse_result.node)
        
        # Step 4: AST visualization (optional)
        visualizer = ASTTextVisualizer()
        ast_output = visualizer.visualize(parse_result.node)
        
        return {
            "stage": "complete",
            "success": analysis_result.success,
            "tokens": token_result.tokens,
            "ast": parse_result.node,
            "symbol_table": analysis_result.symbol_table,
            "errors": analysis_result.errors,
            "warnings": analysis_result.warnings,
            "ast_visualization": ast_output
        }
    
    def test_simple_program_pipeline(self):
        """Test processing a simple program through the complete pipeline."""
        code = """
        Let x be 5
        Let y be 10
        Let sum be x plus y
        Display "Sum is:" with sum
        """
        
        result = self.process_code(code)
        
        assert result["success"]
        assert result["stage"] == "complete"
        assert len(result["errors"]) == 0
        assert result["symbol_table"] is not None
        assert result["ast"] is not None
        
        # Check that symbols were created
        assert result["symbol_table"].lookup("x") is not None
        assert result["symbol_table"].lookup("y") is not None
        assert result["symbol_table"].lookup("sum") is not None
    
    def test_function_definition_pipeline(self):
        """Test processing function definitions through the pipeline."""
        code = """
        Process calculate(a, b) returns number:
            Let result be a plus b
            Return result
        
        Let value be calculate(5, 3)
        Display value
        """
        
        result = self.process_code(code)
        
        assert result["success"]
        assert len(result["errors"]) == 0
        
        # Check function symbol
        func_symbol = result["symbol_table"].lookup("calculate")
        assert func_symbol is not None
        assert len(func_symbol.parameters) == 2
    
    def test_error_detection_pipeline(self):
        """Test that errors are properly detected through the pipeline."""
        code = """
        Let x be undefined_variable
        Set y to 42
        """
        
        result = self.process_code(code)
        
        assert not result["success"]
        assert len(result["errors"]) > 0
        
        # Should detect undefined variable error
        error_messages = [error.message for error in result["errors"]]
        assert any("undefined" in msg.lower() for msg in error_messages)
    
    def test_complex_program_pipeline(self):
        """Test processing a complex program through the pipeline."""
        code = """
        # Mathematical calculation program
        Define pi as 3.14159
        
        Process calculate_area(radius) returns number:
            Return pi multiplied by radius multiplied by radius
        
        Process calculate_circumference(radius) returns number:
            Return 2 multiplied by pi multiplied by radius
        
        Let radius be 5
        Let area be calculate_area(radius)
        Let circumference be calculate_circumference(radius)
        
        Display "Circle with radius:" with radius
        Display "Area:" with area
        Display "Circumference:" with circumference
        """
        
        result = self.process_code(code)
        
        assert result["success"]
        assert len(result["errors"]) == 0
        
        # Check all symbols were created
        symbols = ["pi", "calculate_area", "calculate_circumference", "radius", "area", "circumference"]
        for symbol_name in symbols:
            assert result["symbol_table"].lookup(symbol_name) is not None
    
    def test_control_flow_pipeline(self):
        """Test processing control flow structures through the pipeline."""
        code = """
        Let counter be 0
        
        While counter is less than 5:
            Display "Counter:" with counter
            Set counter to counter plus 1
        
        If counter is equal to 5:
            Display "Loop completed"
        """
        
        result = self.process_code(code)
        
        assert result["success"]
        assert len(result["errors"]) == 0
        
        # Check counter symbol
        counter_symbol = result["symbol_table"].lookup("counter")
        assert counter_symbol is not None
    
    def test_ast_visualization_integration(self):
        """Test that AST visualization works with the pipeline."""
        code = """
        Let x be 5 plus 3
        """
        
        result = self.process_code(code)
        
        assert result["success"]
        assert result["ast_visualization"] is not None
        assert len(result["ast_visualization"]) > 0
        
        # Check that visualization contains expected elements
        viz = result["ast_visualization"]
        assert "Program" in viz
        assert "Declaration" in viz
        assert "BinaryExpression" in viz
        assert "Literal" in viz


class TestLanguageFeatures:
    """Test specific language features through the complete pipeline."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def process_code(self, code: str):
        """Process code through the complete pipeline."""
        lexer = RunaLexer(code)
        token_result = lexer.tokenize()
        
        if not token_result.success:
            return {"success": False, "errors": token_result.errors}
        
        parser = RunaParser(token_result.tokens, self.error_reporter)
        parse_result = parser.parse()
        
        if not parse_result.success:
            return {"success": False, "errors": parse_result.errors}
        
        analyzer = SemanticAnalyzer(self.error_reporter)
        analysis_result = analyzer.analyze(parse_result.node)
        
        return {
            "success": analysis_result.success,
            "symbol_table": analysis_result.symbol_table,
            "errors": analysis_result.errors,
            "warnings": analysis_result.warnings
        }
    
    def test_natural_language_operators(self):
        """Test natural language operators work through the pipeline."""
        code = """
        Let a be 10
        Let b be 5
        
        Let sum be a plus b
        Let difference be a minus b
        Let product be a multiplied by b
        Let quotient be a divided by b
        
        Let is_greater be a is greater than b
        Let is_equal be a is equal to b
        """
        
        result = self.process_code(code)
        
        assert result["success"]
        assert len(result["errors"]) == 0
        
        # All variables should be defined
        variables = ["a", "b", "sum", "difference", "product", "quotient", "is_greater", "is_equal"]
        for var in variables:
            assert result["symbol_table"].lookup(var) is not None
    
    def test_list_operations(self):
        """Test list operations through the pipeline."""
        code = """
        Let numbers be list containing 1, 2, 3, 4, 5
        Let first_number be numbers[0]
        Display "First number:" with first_number
        """
        
        result = self.process_code(code)
        
        assert result["success"]
        assert len(result["errors"]) == 0
        
        # Check symbols
        assert result["symbol_table"].lookup("numbers") is not None
        assert result["symbol_table"].lookup("first_number") is not None
    
    def test_type_annotations(self):
        """Test type annotations through the pipeline."""
        code = """
        Let count (number) be 0
        Let name (string) be "Test"
        Let is_active (boolean) be true
        """
        
        result = self.process_code(code)
        
        assert result["success"]
        # May have warnings about type mismatches, but should not have errors
        
        # Check symbols
        assert result["symbol_table"].lookup("count") is not None
        assert result["symbol_table"].lookup("name") is not None
        assert result["symbol_table"].lookup("is_active") is not None
    
    def test_nested_scopes(self):
        """Test nested scopes through the pipeline."""
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
        
        Call outer_function()
        """
        
        result = self.process_code(code)
        
        assert result["success"]
        assert len(result["errors"]) == 0
        
        # Check that global symbols are accessible
        assert result["symbol_table"].lookup("global_var") is not None
        assert result["symbol_table"].lookup("outer_function") is not None


class TestErrorRecovery:
    """Test error recovery and reporting through the pipeline."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def process_code(self, code: str):
        """Process code through the complete pipeline."""
        lexer = RunaLexer(code)
        token_result = lexer.tokenize()
        
        parser = RunaParser(token_result.tokens, self.error_reporter)
        parse_result = parser.parse()
        
        if parse_result.success:
            analyzer = SemanticAnalyzer(self.error_reporter)
            analysis_result = analyzer.analyze(parse_result.node)
            return analysis_result
        else:
            return parse_result
    
    def test_lexer_error_recovery(self):
        """Test recovery from lexer errors."""
        code = """
        Let x be 5
        Let y be @invalid_token
        Let z be 10
        """
        
        result = self.process_code(code)
        
        # Should have errors but may still parse some parts
        assert not result.success
        assert len(result.errors) > 0
    
    def test_parser_error_recovery(self):
        """Test recovery from parser errors."""
        code = """
        Let x be 5
        Let be 10
        Let z be 15
        """
        
        result = self.process_code(code)
        
        # Should have parsing errors
        assert not result.success
        assert len(result.errors) > 0
    
    def test_semantic_error_recovery(self):
        """Test recovery from semantic errors."""
        code = """
        Let x be 5
        Set undefined_var to 10
        Let y be x plus 3
        """
        
        result = self.process_code(code)
        
        # Should have semantic errors but continue analysis
        assert not result.success
        assert len(result.errors) > 0
        
        # Should still have valid symbols
        assert result.symbol_table.lookup("x") is not None
        assert result.symbol_table.lookup("y") is not None 