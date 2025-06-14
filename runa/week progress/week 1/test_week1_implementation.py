"""
Week 1 Implementation Tests

SECG Compliance: Tests validate ethical operation of all components
Performance Validation: Tests ensure <100ms compilation targets are met
Self-Hosting Readiness: Tests verify components can handle Runa compiler source

This test suite validates the complete Week 1 deliverables:
- Lexer with 50+ token types
- Parser with full Runa syntax support  
- AST nodes for all language constructs
- SECG compliance framework
- Performance targets
"""

import unittest
import time
from typing import List

# Import our Week 1 implementations
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from runa.core import (
    SECGValidator, PerformanceMonitor, RUNA_COMPILATION_TARGET_MS,
    OperationResult, SECGViolationError
)
from runa.core.lexer import RunaLexer, TokenType, Token
from runa.core.parser import RunaParser
from runa.core.ast.ast_nodes import (
    Program, VariableDeclaration, FunctionDefinition, IfStatement,
    BinaryOperation, BinaryOperator, StringLiteral, IntegerLiteral,
    Identifier, DisplayStatement
)

class TestSECGCompliance(unittest.TestCase):
    """Test SECG compliance framework."""
    
    def setUp(self):
        self.secg_validator = SECGValidator()
    
    def test_secg_validator_initialization(self):
        """Test SECG validator initializes correctly."""
        self.assertIsNotNone(self.secg_validator)
        self.assertIsNotNone(self.secg_validator.ethical_logger)
        self.assertIsNotNone(self.secg_validator.harm_assessor)
    
    def test_pre_execution_validation(self):
        """Test pre-execution SECG validation."""
        def safe_operation():
            """A safe operation for testing."""
            return "safe result"
        
        result = self.secg_validator.validate_pre_execution(safe_operation)
        self.assertTrue(result.compliant)
        self.assertTrue(result.secg_validated)
    
    def test_post_execution_validation(self):
        """Test post-execution SECG validation."""
        result = "test result"
        validation = self.secg_validator.validate_post_execution(result)
        self.assertTrue(validation.compliant)

class TestPerformanceMonitoring(unittest.TestCase):
    """Test performance monitoring framework."""
    
    def setUp(self):
        self.monitor = PerformanceMonitor()
    
    def test_performance_target_enforcement(self):
        """Test performance target enforcement."""
        @self.monitor.enforce_target(100)
        def fast_operation():
            return "done"
        
        # Should pass - operation is fast
        result = fast_operation()
        self.assertEqual(result, "done")
    
    def test_performance_violation_detection(self):
        """Test performance violation detection."""
        @self.monitor.enforce_target(1)  # Very strict target
        def slow_operation():
            time.sleep(0.002)  # 2ms delay
            return "slow"
        
        # Should raise PerformanceViolationError
        from runa.core import PerformanceViolationError
        with self.assertRaises(PerformanceViolationError):
            slow_operation()

class TestRunaLexer(unittest.TestCase):
    """Test Runa lexer with complete token coverage."""
    
    def setUp(self):
        self.lexer = RunaLexer()
    
    def test_lexer_initialization(self):
        """Test lexer initializes with all required components."""
        self.assertIsNotNone(self.lexer)
        self.assertGreaterEqual(len(self.lexer.keywords), 50)  # 50+ keywords
        self.assertIsNotNone(self.lexer.performance_monitor)
    
    def test_variable_declaration_tokenization(self):
        """Test tokenization of variable declarations."""
        source = 'Let user name be "Alex"'
        result = self.lexer.tokenize(source)
        
        self.assertTrue(result.success)
        self.assertTrue(result.secg_compliant)
        self.assertIsNotNone(result.execution_time_ms)
        
        tokens = result.value
        self.assertEqual(tokens[0].type, TokenType.LET)
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].value, "user")
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[2].value, "name")
        self.assertEqual(tokens[3].type, TokenType.BE)
        self.assertEqual(tokens[4].type, TokenType.STRING)
        self.assertEqual(tokens[4].value, '"Alex"')
    
    def test_function_definition_tokenization(self):
        """Test tokenization of function definitions."""
        source = '''Process called "Add Numbers" that takes first and second:
    Return first plus second'''
        
        result = self.lexer.tokenize(source)
        self.assertTrue(result.success)
        
        tokens = result.value
        token_types = [token.type for token in tokens]
        
        self.assertIn(TokenType.PROCESS, token_types)
        self.assertIn(TokenType.CALLED, token_types)
        self.assertIn(TokenType.STRING, token_types)
        self.assertIn(TokenType.THAT, token_types)
        self.assertIn(TokenType.TAKES, token_types)
        self.assertIn(TokenType.COLON, token_types)
        self.assertIn(TokenType.INDENT, token_types)
        self.assertIn(TokenType.RETURN, token_types)
        self.assertIn(TokenType.PLUS, token_types)
    
    def test_control_flow_tokenization(self):
        """Test tokenization of control flow statements."""
        source = '''If age is greater than 21:
    Display "Adult"
Otherwise:
    Display "Minor"'''
        
        result = self.lexer.tokenize(source)
        self.assertTrue(result.success)
        
        tokens = result.value
        token_types = [token.type for token in tokens]
        
        self.assertIn(TokenType.IF, token_types)
        self.assertIn(TokenType.IS, token_types)
        self.assertIn(TokenType.GREATER, token_types)
        self.assertIn(TokenType.THAN, token_types)
        self.assertIn(TokenType.OTHERWISE, token_types)
        self.assertIn(TokenType.DISPLAY, token_types)
    
    def test_arithmetic_expressions_tokenization(self):
        """Test tokenization of arithmetic expressions."""
        source = "result be first plus second multiplied by third divided by four"
        
        result = self.lexer.tokenize(source)
        self.assertTrue(result.success)
        
        tokens = result.value
        token_types = [token.type for token in tokens]
        
        self.assertIn(TokenType.PLUS, token_types)
        self.assertIn(TokenType.MULTIPLIED, token_types)
        self.assertIn(TokenType.BY, token_types)
        self.assertIn(TokenType.DIVIDED, token_types)
    
    def test_performance_target_compliance(self):
        """Test lexer meets performance targets."""
        # Generate a moderately large source file
        source = '\n'.join([
            f'Let variable{i} be {i}'
            for i in range(100)
        ])
        
        result = self.lexer.tokenize(source)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.execution_time_ms)
        # Should be well under 100ms for this size
        self.assertLess(result.execution_time_ms, 50)
    
    def test_error_handling(self):
        """Test lexer error handling."""
        # Test with invalid input type
        result = self.lexer.tokenize(123)  # Not a string
        self.assertFalse(result.success)
        self.assertIn("Expected str", result.error)
    
    def test_empty_source_handling(self):
        """Test handling of empty source code."""
        result = self.lexer.tokenize("")
        self.assertTrue(result.success)
        self.assertEqual(len(result.value), 1)  # Just EOF token
        self.assertEqual(result.value[0].type, TokenType.EOF)

class TestRunaParser(unittest.TestCase):
    """Test Runa parser with complete syntax coverage."""
    
    def setUp(self):
        self.lexer = RunaLexer()
        self.parser = RunaParser()
    
    def _parse_source(self, source: str):
        """Helper to tokenize and parse source code."""
        lexer_result = self.lexer.tokenize(source)
        self.assertTrue(lexer_result.success, f"Lexer failed: {lexer_result.error}")
        
        parser_result = self.parser.parse(lexer_result.value)
        self.assertTrue(parser_result.success, f"Parser failed: {parser_result.error}")
        
        return parser_result.value
    
    def test_variable_declaration_parsing(self):
        """Test parsing of variable declarations."""
        source = 'Let user name be "Alex"'
        program = self._parse_source(source)
        
        self.assertIsInstance(program, Program)
        self.assertEqual(len(program.statements), 1)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertEqual(stmt.name, "user")  # Note: parser should handle this correctly
        self.assertEqual(stmt.declaration_type, "Let")
        self.assertIsInstance(stmt.value, StringLiteral)
    
    def test_function_definition_parsing(self):
        """Test parsing of function definitions."""
        source = '''Process called "Add Numbers" that takes first and second:
    Return first plus second'''
        
        program = self._parse_source(source)
        
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, FunctionDefinition)
        self.assertEqual(stmt.name, "Add Numbers")
        self.assertEqual(len(stmt.parameters), 2)
        self.assertEqual(stmt.parameters[0].name, "first")
        self.assertEqual(stmt.parameters[1].name, "second")
    
    def test_if_statement_parsing(self):
        """Test parsing of if statements."""
        source = '''If age is greater than 21:
    Display "Adult"
Otherwise:
    Display "Minor"'''
        
        program = self._parse_source(source)
        
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, IfStatement)
        self.assertIsNotNone(stmt.condition)
        self.assertIsNotNone(stmt.then_block)
        self.assertIsNotNone(stmt.else_block)
    
    def test_binary_operation_parsing(self):
        """Test parsing of binary operations."""
        source = 'Let result be first plus second'
        program = self._parse_source(source)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertIsInstance(stmt.value, BinaryOperation)
        self.assertEqual(stmt.value.operator, BinaryOperator.PLUS)
    
    def test_display_statement_parsing(self):
        """Test parsing of display statements."""
        source = 'Display "Hello, World!"'
        program = self._parse_source(source)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, DisplayStatement)
        self.assertEqual(len(stmt.expressions), 1)
        self.assertIsInstance(stmt.expressions[0], StringLiteral)
    
    def test_performance_target_compliance(self):
        """Test parser meets performance targets."""
        # Generate a moderately complex program
        source = '''Process called "Complex Function" that takes data:
    Let result be 0
    For each item in data:
        If item is greater than 10:
            Set result be result plus item
        Otherwise:
            Set result be result minus item
    Return result

Let numbers be list containing 1, 2, 3, 4, 5
Let final be Complex Function with data as numbers
Display final'''
        
        lexer_result = self.lexer.tokenize(source)
        self.assertTrue(lexer_result.success)
        
        parser_result = self.parser.parse(lexer_result.value)
        self.assertTrue(parser_result.success)
        self.assertIsNotNone(parser_result.execution_time_ms)
        # Should be well under 100ms
        self.assertLess(parser_result.execution_time_ms, 100)
    
    def test_error_handling(self):
        """Test parser error handling."""
        # Test with invalid input
        result = self.parser.parse("not a list")
        self.assertFalse(result.success)
        
        # Test with empty token list
        result = self.parser.parse([])
        self.assertTrue(result.success)
        self.assertIsInstance(result.value, Program)
        self.assertEqual(len(result.value.statements), 0)

class TestIntegration(unittest.TestCase):
    """Integration tests for complete compilation pipeline."""
    
    def setUp(self):
        self.lexer = RunaLexer()
        self.parser = RunaParser()
    
    def test_complete_program_compilation(self):
        """Test complete program from source to AST."""
        source = '''# Simple Runa program
Let greeting be "Hello, Runa!"
Display greeting

Process called "Greet User" that takes name:
    Let message be "Hello, " plus name
    Display message
    Return message

Let user name be "Developer"
Let result be Greet User with name as user name'''
        
        # Tokenize
        lexer_result = self.lexer.tokenize(source)
        self.assertTrue(lexer_result.success)
        self.assertTrue(lexer_result.secg_compliant)
        
        # Parse
        parser_result = self.parser.parse(lexer_result.value)
        self.assertTrue(parser_result.success)
        self.assertTrue(parser_result.secg_compliant)
        
        # Validate AST structure
        program = parser_result.value
        self.assertIsInstance(program, Program)
        self.assertGreater(len(program.statements), 0)
        
        # Check for expected statement types
        statement_types = [type(stmt).__name__ for stmt in program.statements]
        self.assertIn('VariableDeclaration', statement_types)
        self.assertIn('DisplayStatement', statement_types)
        self.assertIn('FunctionDefinition', statement_types)
    
    def test_natural_language_constructs(self):
        """Test natural language programming constructs."""
        source = '''Let age be 25
If age is greater than 18 and age is less than 65:
    Display "Working age"
    
Let items be list containing "apple", "banana", "cherry"
For each fruit in items:
    Display fruit with message "is delicious"
    
Match age:
    When 18:
        Display "Just became adult"
    When _:
        Display "Other age"'''
        
        lexer_result = self.lexer.tokenize(source)
        self.assertTrue(lexer_result.success)
        
        parser_result = self.parser.parse(lexer_result.value)
        self.assertTrue(parser_result.success)
        
        program = parser_result.value
        self.assertIsInstance(program, Program)
        # Should have parsed all major constructs without errors
        self.assertGreater(len(program.statements), 3)
    
    def test_performance_targets_met(self):
        """Test that complete pipeline meets performance targets."""
        # Generate a substantial program
        lines = [
            "# Performance test program",
            "Let counter be 0"
        ]
        
        # Add many variable declarations
        for i in range(50):
            lines.append(f'Let var{i} be {i}')
        
        # Add a function
        lines.extend([
            'Process called "Sum Numbers" that takes numbers:',
            '    Let total be 0',
            '    For each num in numbers:',
            '        Set total be total plus num',
            '    Return total'
        ])
        
        # Add function calls
        for i in range(10):
            lines.append(f'Let result{i} be Sum Numbers with numbers as list containing 1, 2, 3')
        
        source = '\n'.join(lines)
        
        start_time = time.perf_counter()
        
        # Complete compilation pipeline
        lexer_result = self.lexer.tokenize(source)
        self.assertTrue(lexer_result.success)
        
        parser_result = self.parser.parse(lexer_result.value)
        self.assertTrue(parser_result.success)
        
        end_time = time.perf_counter()
        total_time_ms = (end_time - start_time) * 1000
        
        # Should meet the 100ms target for 1000-line programs
        # This is much smaller, so should be very fast
        self.assertLess(total_time_ms, RUNA_COMPILATION_TARGET_MS)
        
        print(f"Complete compilation took {total_time_ms:.1f}ms (target: <{RUNA_COMPILATION_TARGET_MS}ms)")

class TestSelfHostingReadiness(unittest.TestCase):
    """Test readiness for self-hosting capability."""
    
    def setUp(self):
        self.lexer = RunaLexer()
        self.parser = RunaParser()
    
    def test_can_parse_compiler_like_code(self):
        """Test parsing of code that resembles a compiler."""
        compiler_source = '''# Simplified compiler structure in Runa

Type Token is Dictionary with:
    type as String
    value as String
    line as Integer

Process called "Tokenize" that takes source:
    Let tokens be list containing
    Let position be 0
    
    While position is less than length of source:
        Let char be character at position in source
        If char is equal to " ":
            # Skip whitespace
            Set position be position plus 1
        Otherwise:
            # Create token
            Let token be Token with type as "CHAR" and value as char
            # Add to tokens list
            Set position be position plus 1
    
    Return tokens

Process called "Parse" that takes tokens:
    Let ast be list containing
    For each token in tokens:
        # Simple parsing logic
        If token type is equal to "CHAR":
            # Add to AST
            Pass  # Placeholder
    Return ast

Process called "Compile" that takes source:
    Let tokens be Tokenize with source as source
    Let ast be Parse with tokens as tokens
    Return ast'''
        
        # This should tokenize and parse without errors
        lexer_result = self.lexer.tokenize(compiler_source)
        self.assertTrue(lexer_result.success, f"Lexer error: {lexer_result.error}")
        
        parser_result = self.parser.parse(lexer_result.value)
        self.assertTrue(parser_result.success, f"Parser error: {parser_result.error}")
        
        program = parser_result.value
        self.assertIsInstance(program, Program)
        
        # Should have multiple function definitions
        functions = [stmt for stmt in program.statements if isinstance(stmt, FunctionDefinition)]
        self.assertGreaterEqual(len(functions), 3)
        
        # Function names should match expected
        function_names = [func.name for func in functions]
        self.assertIn("Tokenize", function_names)
        self.assertIn("Parse", function_names)
        self.assertIn("Compile", function_names)

if __name__ == '__main__':
    # Configure test output
    import sys
    
    print("=" * 70)
    print("RUNA WEEK 1 IMPLEMENTATION TESTS")
    print("=" * 70)
    print("Testing SECG compliance, performance targets, and functionality")
    print("Target: <100ms compilation for 1000-line programs")
    print("=" * 70)
    
    # Run tests with verbose output
    unittest.main(verbosity=2, buffer=True) 