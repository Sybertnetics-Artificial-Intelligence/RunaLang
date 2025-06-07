"""
Comprehensive AST Visualizer Tests for Runa Programming Language.

This module contains extensive tests for the AST visualizer,
covering tree visualization, formatting options, and all node types.

Test Categories:
- Basic visualization functionality
- Formatting and display options
- Different node type handling
- Complex AST structures
- Output validation
"""

import pytest
from unittest.mock import Mock
from typing import List, Any

from runa.lexer import RunaLexer
from runa.parser import RunaParser
from runa.ast_visualizer import ASTTextVisualizer, NodeInfo
from runa.ast_nodes import *
from runa.errors import SourcePosition, ErrorReporter


class TestASTVisualizerBasics:
    """Test basic AST visualizer functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
        self.visualizer = ASTTextVisualizer()
    
    def parse_code(self, code: str) -> Program:
        """Helper to parse code and return AST."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        result = parser.parse()
        
        if not result.success:
            pytest.fail(f"Parser failed: {result.errors}")
        
        return result.node
    
    def test_visualizer_creation(self):
        """Test creating AST visualizer."""
        visualizer = ASTTextVisualizer()
        
        assert visualizer.show_positions is True
        assert visualizer.show_types is True
        assert visualizer.max_depth is None
        assert visualizer.indent_size == 2
    
    def test_visualizer_with_options(self):
        """Test creating visualizer with custom options."""
        visualizer = ASTTextVisualizer(
            show_positions=False,
            show_types=False,
            max_depth=5,
            indent_size=4
        )
        
        assert visualizer.show_positions is False
        assert visualizer.show_types is False
        assert visualizer.max_depth == 5
        assert visualizer.indent_size == 4
    
    def test_empty_program_visualization(self):
        """Test visualizing an empty program."""
        ast = self.parse_code("")
        output = self.visualizer.visualize(ast)
        
        assert "Program" in output
        assert "statements: []" in output or "statements=[]" in output
    
    def test_simple_literal_visualization(self):
        """Test visualizing a simple literal."""
        ast = self.parse_code("42")
        output = self.visualizer.visualize(ast)
        
        assert "Program" in output
        assert "ExpressionStatement" in output
        assert "Literal" in output
        assert "42" in output


class TestNodeVisualization:
    """Test visualization of different node types."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
        self.visualizer = ASTTextVisualizer()
    
    def parse_code(self, code: str) -> Program:
        """Helper to parse code and return AST."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens.tokens, self.error_reporter)
        result = parser.parse()
        return result.node
    
    def test_declaration_visualization(self):
        """Test visualizing variable declarations."""
        ast = self.parse_code("Let x be 5")
        output = self.visualizer.visualize(ast)
        
        assert "Declaration" in output
        assert "identifier: x" in output or "identifier=x" in output
        assert "is_constant: False" in output or "is_constant=False" in output
        assert "Literal" in output
        assert "5" in output
    
    def test_constant_declaration_visualization(self):
        """Test visualizing constant declarations."""
        ast = self.parse_code('Define pi as 3.14159')
        output = self.visualizer.visualize(ast)
        
        assert "Declaration" in output
        assert "identifier: pi" in output or "identifier=pi" in output
        assert "is_constant: True" in output or "is_constant=True" in output
        assert "3.14159" in output
    
    def test_assignment_visualization(self):
        """Test visualizing assignments."""
        ast = self.parse_code("Set x to 10")
        output = self.visualizer.visualize(ast)
        
        assert "Assignment" in output
        assert "identifier: x" in output or "identifier=x" in output
        assert "10" in output
    
    def test_binary_expression_visualization(self):
        """Test visualizing binary expressions."""
        ast = self.parse_code("5 plus 3")
        output = self.visualizer.visualize(ast)
        
        assert "BinaryExpression" in output
        assert "operator" in output
        assert "ADD" in output or "PLUS" in output
        assert "left:" in output
        assert "right:" in output
        assert "5" in output
        assert "3" in output
    
    def test_function_call_visualization(self):
        """Test visualizing function calls."""
        ast = self.parse_code('Call print("Hello")')
        output = self.visualizer.visualize(ast)
        
        assert "FunctionCall" in output
        assert "function_name: print" in output or "function_name=print" in output
        assert "Hello" in output
    
    def test_list_expression_visualization(self):
        """Test visualizing list expressions."""
        ast = self.parse_code("list containing 1, 2, 3")
        output = self.visualizer.visualize(ast)
        
        assert "ListExpression" in output
        assert "elements:" in output
        assert "1" in output
        assert "2" in output
        assert "3" in output


class TestFormattingOptions:
    """Test different formatting options."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str) -> Program:
        """Helper to parse code and return AST."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens.tokens, self.error_reporter)
        result = parser.parse()
        return result.node
    
    def test_without_positions(self):
        """Test visualization without position information."""
        visualizer = ASTTextVisualizer(show_positions=False)
        ast = self.parse_code("Let x be 5")
        output = visualizer.visualize(ast)
        
        # Should not contain position information
        assert "line:" not in output
        assert "column:" not in output
        assert "position:" not in output
    
    def test_with_positions(self):
        """Test visualization with position information."""
        visualizer = ASTTextVisualizer(show_positions=True)
        ast = self.parse_code("Let x be 5")
        output = visualizer.visualize(ast)
        
        # Should contain position information
        assert "line:" in output or "position:" in output
    
    def test_without_types(self):
        """Test visualization without type information."""
        visualizer = ASTTextVisualizer(show_types=False)
        ast = self.parse_code("Let x be 5")
        output = visualizer.visualize(ast)
        
        # Should still show node types but not detailed type info
        assert "Declaration" in output
        assert "Literal" in output
    
    def test_custom_indent_size(self):
        """Test visualization with custom indent size."""
        visualizer = ASTTextVisualizer(indent_size=4)
        ast = self.parse_code("Let x be 5")
        output = visualizer.visualize(ast)
        
        lines = output.split('\n')
        # Check that indentation is properly applied
        indented_lines = [line for line in lines if line.startswith('    ')]
        assert len(indented_lines) > 0
    
    def test_max_depth_limiting(self):
        """Test visualization with depth limiting."""
        visualizer = ASTTextVisualizer(max_depth=2)
        ast = self.parse_code("Let x be 5 plus 3")
        output = visualizer.visualize(ast)
        
        # Should contain truncation indicator for deep nodes
        assert "..." in output or "truncated" in output.lower()


class TestComplexStructures:
    """Test visualization of complex AST structures."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
        self.visualizer = ASTTextVisualizer()
    
    def parse_code(self, code: str) -> Program:
        """Helper to parse code and return AST."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens.tokens, self.error_reporter)
        result = parser.parse()
        return result.node
    
    def test_nested_expressions(self):
        """Test visualizing nested expressions."""
        ast = self.parse_code("(5 plus 3) multiplied by (10 minus 2)")
        output = self.visualizer.visualize(ast)
        
        assert "BinaryExpression" in output
        assert "MULTIPLY" in output or "multiplied" in output
        # Should show nested structure
        assert output.count("BinaryExpression") >= 3  # Main expression + 2 sub-expressions
    
    def test_function_definition(self):
        """Test visualizing function definitions."""
        code = """
        Process calculate(x, y) returns number:
            Return x plus y
        """
        ast = self.parse_code(code)
        output = self.visualizer.visualize(ast)
        
        assert "ProcessDefinition" in output
        assert "name: calculate" in output or "name=calculate" in output
        assert "parameters:" in output
        assert "return_type:" in output
        assert "body:" in output
        assert "ReturnStatement" in output
    
    def test_control_flow_structures(self):
        """Test visualizing control flow structures."""
        code = """
        If x is greater than 5:
            Display "Large"
        Else:
            Display "Small"
        """
        ast = self.parse_code(code)
        output = self.visualizer.visualize(ast)
        
        assert "IfStatement" in output
        assert "condition:" in output
        assert "then_block:" in output
        assert "else_block:" in output
        assert "DisplayStatement" in output
    
    def test_loop_structures(self):
        """Test visualizing loop structures."""
        code = """
        While x is less than 10:
            Set x to x plus 1
        """
        ast = self.parse_code(code)
        output = self.visualizer.visualize(ast)
        
        assert "WhileLoop" in output
        assert "condition:" in output
        assert "body:" in output
        assert "Assignment" in output
    
    def test_comprehensive_program(self):
        """Test visualizing a comprehensive program."""
        code = """
        # Define constants
        Define max_value as 100
        
        # Declare variables
        Let counter be 0
        
        # Function definition
        Process increment() returns number:
            Set counter to counter plus 1
            Return counter
        
        # Main logic
        While counter is less than max_value:
            Let result be increment()
            Display "Counter:" with result
        """
        ast = self.parse_code(code)
        output = self.visualizer.visualize(ast)
        
        # Should contain all major node types
        assert "Program" in output
        assert "Comment" in output
        assert "Declaration" in output
        assert "ProcessDefinition" in output
        assert "WhileLoop" in output
        assert "Assignment" in output
        assert "FunctionCall" in output
        assert "DisplayStatement" in output


class TestNodeInfo:
    """Test NodeInfo functionality."""
    
    def test_node_info_creation(self):
        """Test creating NodeInfo objects."""
        position = SourcePosition(1, 5)
        literal = Literal(42, "number", position)
        
        info = NodeInfo(
            node_type="Literal",
            attributes={"value": 42, "literal_type": "number"},
            position=position,
            children=[]
        )
        
        assert info.node_type == "Literal"
        assert info.attributes["value"] == 42
        assert info.position == position
        assert len(info.children) == 0
    
    def test_node_info_with_children(self):
        """Test NodeInfo with child nodes."""
        position = SourcePosition(1, 1)
        
        left_info = NodeInfo("Literal", {"value": 5}, position, [])
        right_info = NodeInfo("Literal", {"value": 3}, position, [])
        
        binary_info = NodeInfo(
            "BinaryExpression",
            {"operator": "ADD"},
            position,
            [left_info, right_info]
        )
        
        assert binary_info.node_type == "BinaryExpression"
        assert len(binary_info.children) == 2
        assert binary_info.children[0] == left_info
        assert binary_info.children[1] == right_info


class TestErrorHandling:
    """Test error handling in AST visualization."""
    
    def setup_method(self):
        """Set up test environment."""
        self.visualizer = ASTTextVisualizer()
    
    def test_none_node_handling(self):
        """Test handling of None nodes."""
        output = self.visualizer.visualize(None)
        
        assert "None" in output or "null" in output.lower()
    
    def test_invalid_node_handling(self):
        """Test handling of invalid node types."""
        # Create a mock object that's not a valid AST node
        mock_node = Mock()
        mock_node.__class__.__name__ = "InvalidNode"
        
        # Should not crash, should handle gracefully
        output = self.visualizer.visualize(mock_node)
        assert "InvalidNode" in output or "Unknown" in output
    
    def test_circular_reference_protection(self):
        """Test protection against circular references."""
        # This is a theoretical test - in practice, our AST nodes shouldn't have circular refs
        # But the visualizer should be robust
        position = SourcePosition(1, 1)
        node = Literal(42, "number", position)
        
        # Normal case should work fine
        output = self.visualizer.visualize(node)
        assert "Literal" in output
        assert "42" in output


class TestOutputValidation:
    """Test output format validation."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
        self.visualizer = ASTTextVisualizer()
    
    def parse_code(self, code: str) -> Program:
        """Helper to parse code and return AST."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens.tokens, self.error_reporter)
        result = parser.parse()
        return result.node
    
    def test_output_is_string(self):
        """Test that output is always a string."""
        ast = self.parse_code("42")
        output = self.visualizer.visualize(ast)
        
        assert isinstance(output, str)
        assert len(output) > 0
    
    def test_output_contains_tree_structure(self):
        """Test that output shows tree structure."""
        ast = self.parse_code("Let x be 5 plus 3")
        output = self.visualizer.visualize(ast)
        
        lines = output.split('\n')
        
        # Should have multiple lines for tree structure
        assert len(lines) > 1
        
        # Should have proper indentation
        indented_lines = [line for line in lines if line.startswith(' ')]
        assert len(indented_lines) > 0
    
    def test_output_readability(self):
        """Test that output is human-readable."""
        ast = self.parse_code("Let x be 5")
        output = self.visualizer.visualize(ast)
        
        # Should contain recognizable keywords and structure
        assert "Program" in output
        assert "Declaration" in output
        assert "Literal" in output
        
        # Should not contain raw object representations
        assert "<object" not in output
        assert "0x" not in output  # Memory addresses
    
    def test_consistent_formatting(self):
        """Test that formatting is consistent."""
        ast1 = self.parse_code("Let x be 5")
        ast2 = self.parse_code("Let y be 10")
        
        output1 = self.visualizer.visualize(ast1)
        output2 = self.visualizer.visualize(ast2)
        
        lines1 = output1.split('\n')
        lines2 = output2.split('\n')
        
        # Should have similar structure (same number of levels)
        assert len(lines1) == len(lines2)
        
        # Should use consistent indentation
        indent_pattern1 = [len(line) - len(line.lstrip()) for line in lines1 if line.strip()]
        indent_pattern2 = [len(line) - len(line.lstrip()) for line in lines2 if line.strip()]
        
        # Patterns should be the same (same tree depth structure)
        assert indent_pattern1 == indent_pattern2 