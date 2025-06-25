"""
Runa Compiler Test Suite

Comprehensive tests for the Runa compiler covering:
- Lexical analysis with natural language support
- Recursive descent parsing with error recovery
- Vector-based semantic analysis
- Multi-pass bytecode generation with optimization
- Performance validation for <100ms compilation target
"""

import unittest
import time
from typing import List, Dict, Any

from runa.compiler import (
    Compiler, Lexer, Parser, SemanticAnalyzer, BytecodeGenerator,
    Token, TokenType, ASTNode, Program, Statement, Expression,
    VariableDeclaration, FunctionDeclaration, Identifier, Literal,
    BinaryExpression, CallExpression, IfStatement, ForStatement,
    WhileStatement, ReturnStatement, TypeAnnotation, Parameter
)


class TestLexer(unittest.TestCase):
    """Test lexical analysis with natural language support."""
    
    def setUp(self):
        self.lexer = Lexer()
    
    def test_basic_tokens(self):
        """Test basic token recognition."""
        source = "let x be 42"
        tokens = self.lexer.tokenize(source)
        
        expected_types = [
            TokenType.LET,
            TokenType.IDENTIFIER,
            TokenType.BE,
            TokenType.INTEGER,
            TokenType.EOF
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for token, expected_type in zip(tokens, expected_types):
            self.assertEqual(token.type, expected_type)
    
    def test_natural_language_operators(self):
        """Test natural language operator recognition."""
        source = "x multiplied by y plus z"
        tokens = self.lexer.tokenize(source)
        
        expected_types = [
            TokenType.IDENTIFIER,
            TokenType.MULTIPLY,
            TokenType.BY,
            TokenType.IDENTIFIER,
            TokenType.PLUS,
            TokenType.IDENTIFIER,
            TokenType.EOF
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for token, expected_type in zip(tokens, expected_types):
            self.assertEqual(token.type, expected_type)
    
    def test_ai_blocks(self):
        """Test AI-specific block recognition."""
        source = "@reasoning This is AI reasoning\n@end"
        tokens = self.lexer.tokenize(source)
        
        expected_types = [
            TokenType.REASONING,
            TokenType.TYPE_IDENTIFIER,  # "This" - capitalized
            TokenType.IS,
            TokenType.TYPE_IDENTIFIER,  # "AI" - capitalized
            TokenType.IDENTIFIER,  # "reasoning" - lowercase
            TokenType.NEWLINE,
            TokenType.END,
            TokenType.EOF
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for token, expected_type in zip(tokens, expected_types):
            self.assertEqual(token.type, expected_type)
    
    def test_indentation_handling(self):
        """Test indentation and whitespace handling."""
        source = """
        let x be 1
            let y be 2
                let z be 3
        """
        tokens = self.lexer.tokenize(source)
        
        # Should handle indentation correctly
        self.assertGreater(len(tokens), 0)
        self.assertEqual(tokens[-1].type, TokenType.EOF)
    
    def test_error_recovery(self):
        """Test error recovery in lexer."""
        source = "let x be 42 @invalid_token"
        tokens = self.lexer.tokenize(source)
        
        # Should recover and continue parsing
        self.assertGreater(len(tokens), 0)
        self.assertEqual(tokens[-1].type, TokenType.EOF)


class TestParser(unittest.TestCase):
    """Test recursive descent parsing with error recovery."""
    
    def setUp(self):
        self.parser = Parser()
    
    def test_variable_declaration(self):
        """Test variable declaration parsing."""
        source = "let x be 42"
        tokens = self.parser.lexer.tokenize(source)
        ast = self.parser.parse(tokens)
        
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertEqual(stmt.name, "x")
        self.assertIsInstance(stmt.value, Literal)
        self.assertEqual(stmt.value.value, 42)
    
    def test_function_declaration(self):
        """Test function declaration parsing."""
        source = """
        process called add with x as Integer and y as Integer returning Integer:
            let result be x plus y
            return result
        """
        tokens = self.parser.lexer.tokenize(source)
        # Debug print: show all token types and values
        print('TOKENS:', [(t.type.name, t.value) for t in tokens])
        ast = self.parser.parse(tokens)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, FunctionDeclaration)
        self.assertEqual(stmt.name, "add")
        self.assertEqual(len(stmt.parameters), 2)
    
    def test_binary_expressions(self):
        """Test binary expression parsing."""
        source = "let result be x multiplied by y plus z"
        tokens = self.parser.lexer.tokenize(source)
        ast = self.parser.parse(tokens)
        
        self.assertIsInstance(ast, Program)
        stmt = ast.statements[0]
        self.assertIsInstance(stmt.value, BinaryExpression)
    
    def test_control_flow(self):
        """Test control flow statement parsing."""
        source = """
        if x is greater than 0:
            Display "Positive"
        otherwise:
            Display "Negative"
        """
        tokens = self.parser.lexer.tokenize(source)
        ast = self.parser.parse(tokens)
        
        self.assertIsInstance(ast, Program)
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, IfStatement)
    
    def test_error_recovery(self):
        """Test parser error recovery."""
        source = "let x be 42 let y be"  # Incomplete statement
        tokens = self.parser.lexer.tokenize(source)
        
        # Should recover and continue parsing
        ast = self.parser.parse(tokens)
        self.assertIsInstance(ast, Program)


class TestSemanticAnalyzer(unittest.TestCase):
    """Test vector-based semantic analysis."""
    
    def setUp(self):
        self.analyzer = SemanticAnalyzer()
    
    def test_variable_declaration_analysis(self):
        """Test variable declaration semantic analysis."""
        # Create AST manually
        program = Program(1, 1, None, statements=[
            VariableDeclaration(
                name="x",
                value=Literal(value=42, literal_type="integer", line=1, column=1),
                type_annotation=None,
                is_constant=False,
                line=1,
                column=1
            )
        ])
        
        success = self.analyzer.analyze(program)
        self.assertTrue(success)
        self.assertEqual(len(self.analyzer.get_errors()), 0)
    
    def test_type_checking(self):
        """Test type checking and validation."""
        program = Program(1, 1, None, statements=[
            VariableDeclaration(
                name="x",
                type_annotation=TypeAnnotation(type_name="Integer", line=1, column=1),
                value=Literal(value="not a number", literal_type="string", line=1, column=1),
                is_constant=False,
                line=1,
                column=1
            )
        ])
        
        success = self.analyzer.analyze(program)
        self.assertFalse(success)  # Should fail due to type mismatch
        self.assertGreater(len(self.analyzer.get_errors()), 0)
    
    def test_undefined_variable(self):
        """Test undefined variable detection."""
        program = Program(1, 1, None, statements=[
            VariableDeclaration(
                name="x",
                value=Identifier(name="undefined_var", line=1, column=1),
                type_annotation=None,
                is_constant=False,
                line=1,
                column=1
            )
        ])
        
        success = self.analyzer.analyze(program)
        self.assertFalse(success)  # Should fail due to undefined variable
        self.assertGreater(len(self.analyzer.get_errors()), 0)
    
    def test_function_analysis(self):
        """Test function declaration analysis."""
        program = Program(1, 1, None, statements=[
            FunctionDeclaration(
                name="add",
                parameters=[
                    Parameter(
                        name="x",
                        type_annotation=TypeAnnotation(type_name="Integer", line=1, column=1)
                    )
                ],
                return_type=TypeAnnotation(type_name="Integer", line=1, column=1),
                body=[],
                line=1,
                column=1
            )
        ])
        
        success = self.analyzer.analyze(program)
        self.assertTrue(success)
        self.assertEqual(len(self.analyzer.get_errors()), 0)
    
    def test_semantic_disambiguation(self):
        """Test vector-based semantic disambiguation with production implementation."""
        # Test semantic disambiguation with real vector analysis
        program = Program(1, 1, None, statements=[
            VariableDeclaration(
                name="x",
                value=Literal(value=42, literal_type="integer", line=1, column=1),
                type_annotation=None,
                is_constant=False,
                line=1,
                column=1
            ),
            VariableDeclaration(
                name="y",
                value=Literal(value=10, literal_type="integer", line=2, column=1),
                type_annotation=None,
                is_constant=False,
                line=2,
                column=1
            )
        ])
        
        success = self.analyzer.analyze(program)
        self.assertTrue(success)
        
        # Test vector engine functionality
        vector_engine = self.analyzer.vector_engine
        embedding = vector_engine.generate_embedding("test")
        self.assertIsInstance(embedding, list)
        self.assertGreater(len(embedding), 0)
        
        # Test semantic pattern analysis
        patterns = vector_engine.analyze_semantic_patterns("let x be 42 plus 10")
        self.assertIn('mathematical_operation', patterns)
        self.assertGreater(patterns['mathematical_operation'], 0.0)


class TestBytecodeGenerator(unittest.TestCase):
    """Test bytecode generation with optimization."""
    
    def setUp(self):
        self.semantic_analyzer = SemanticAnalyzer()
        self.generator = BytecodeGenerator()
        self.generator.set_semantic_analyzer(self.semantic_analyzer)
    
    def test_simple_program_generation(self):
        """Test bytecode generation for simple program."""
        program = Program(1, 1, None, statements=[
            VariableDeclaration(
                name="x",
                value=Literal(value=42, literal_type="integer", line=1, column=1),
                type_annotation=None,
                is_constant=False,
                line=1,
                column=1
            )
        ])
        
        # Analyze first
        self.semantic_analyzer.analyze(program)
        
        # Generate bytecode
        bytecode = self.generator.generate(program)
        
        self.assertIsNotNone(bytecode)
        self.assertIsNotNone(bytecode.main_function)
        self.assertGreater(len(bytecode.main_function.bytecode), 0)
    
    def test_function_generation(self):
        """Test function bytecode generation."""
        program = Program(1, 1, None, statements=[
            FunctionDeclaration(
                name="add",
                parameters=[
                    Parameter(
                        name="x",
                        type_annotation=TypeAnnotation(type_name="Integer", line=1, column=1)
                    )
                ],
                return_type=TypeAnnotation(type_name="Integer", line=1, column=1),
                body=[
                    ReturnStatement(
                        value=Identifier(name="x", line=2, column=1),
                        line=2,
                        column=1
                    )
                ],
                line=1,
                column=1
            )
        ])
        
        # Analyze first
        self.semantic_analyzer.analyze(program)
        
        # Generate bytecode
        bytecode = self.generator.generate(program)
        
        self.assertIsNotNone(bytecode)
        self.assertIn("add", bytecode.functions)
        func = bytecode.functions["add"]
        self.assertGreater(len(func.bytecode), 0)
    
    def test_optimization_passes(self):
        """Test that optimization passes are applied."""
        program = Program(1, 1, None, statements=[
            VariableDeclaration(
                name="x",
                value=BinaryExpression(
                    left=Literal(value=2, literal_type="integer", line=1, column=1),
                    operator="*",
                    right=Literal(value=3, literal_type="integer", line=1, column=1),
                    line=1,
                    column=1
                ),
                type_annotation=None,
                is_constant=False,
                line=1,
                column=1
            )
        ])
        
        # Analyze first
        self.semantic_analyzer.analyze(program)
        
        # Generate bytecode
        bytecode = self.generator.generate(program)
        
        # Check that optimizations were applied
        metrics = self.generator.get_performance_metrics()
        self.assertGreater(metrics['optimization_time_ms'], 0)
    
    def test_performance_metrics(self):
        """Test performance metrics collection."""
        program = Program(1, 1, None, statements=[
            VariableDeclaration(
                name="x",
                value=Literal(value=42, literal_type="integer", line=1, column=1),
                type_annotation=None,
                is_constant=False,
                line=1,
                column=1
            )
        ])
        
        # Analyze first
        self.semantic_analyzer.analyze(program)
        
        # Generate bytecode
        bytecode = self.generator.generate(program)
        
        # Check metrics
        metrics = self.generator.get_performance_metrics()
        self.assertIn('generation_time_ms', metrics)
        self.assertIn('instruction_count', metrics)
        self.assertIn('constant_count', metrics)


class TestCompilerIntegration(unittest.TestCase):
    """Test complete compiler integration."""
    
    def setUp(self):
        self.compiler = Compiler()
    
    def test_end_to_end_compilation(self):
        """Test complete compilation pipeline."""
        source_code = """
        let x be 42
        let y be 10
        let result be x plus y
        Display result
        """
        
        bytecode = self.compiler.compile(source_code)
        
        self.assertIsNotNone(bytecode)
        self.assertIsNotNone(bytecode.main_function)
        self.assertGreater(len(bytecode.main_function.bytecode), 0)
    
    def test_performance_target(self):
        """Test that compilation meets <100ms performance target."""
        source_code = """
        let x be 42
        let y be 10
        let result be x plus y
        Display result
        """
        
        bytecode = self.compiler.compile(source_code)
        
        # Check performance
        self.assertTrue(self.compiler.validate_performance_target())
        
        metrics = self.compiler.get_performance_metrics()
        self.assertLess(metrics['total_compilation_time_ms'], 100.0)
    
    def test_error_handling(self):
        """Test error handling in complete pipeline."""
        source_code = """
        let x be undefined_variable
        """
        
        with self.assertRaises(Exception):
            self.compiler.compile(source_code)
    
    def test_complex_program(self):
        """Test compilation of more complex program."""
        source_code = """
        process called factorial with n as Integer returning Integer:
            if n is equal to 0:
                return 1
            otherwise:
                let result be n multiplied by factorial with n minus 1
                return result
        
        let x be 5
        let result be factorial with x
        Display result
        """
        
        bytecode = self.compiler.compile(source_code)
        
        self.assertIsNotNone(bytecode)
        self.assertIn("factorial", bytecode.functions)
        self.assertIsNotNone(bytecode.main_function)
    
    def test_natural_language_features(self):
        """Test natural language feature compilation."""
        source_code = """
        let x be 10
        let y be 5
        let result be x multiplied by y plus 2
        Display "The result is" followed by result
        """
        
        bytecode = self.compiler.compile(source_code)
        
        self.assertIsNotNone(bytecode)
        self.assertIsNotNone(bytecode.main_function)
        self.assertGreater(len(bytecode.main_function.bytecode), 0)


class TestPerformanceBenchmarks(unittest.TestCase):
    """Performance benchmarks for compiler."""
    
    def setUp(self):
        self.compiler = Compiler()
    
    def test_compilation_speed(self):
        """Benchmark compilation speed."""
        source_code = """
        let x be 42
        let y be 10
        let result be x plus y
        Display result
        """
        
        # Run multiple compilations to get average
        times = []
        for _ in range(10):
            start_time = time.perf_counter()
            bytecode = self.compiler.compile(source_code)
            end_time = time.perf_counter()
            times.append((end_time - start_time) * 1000)
        
        avg_time = sum(times) / len(times)
        self.assertLess(avg_time, 100.0, f"Average compilation time {avg_time:.2f}ms exceeds 100ms target")
    
    def test_memory_usage(self):
        """Test memory usage during compilation."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        source_code = """
        let x be 42
        let y be 10
        let result be x plus y
        Display result
        """
        
        # Compile multiple times
        for _ in range(100):
            bytecode = self.compiler.compile(source_code)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (< 100MB)
        self.assertLess(memory_increase, 100 * 1024 * 1024, 
                       f"Memory increase {memory_increase / (1024*1024):.2f}MB exceeds 100MB limit")


if __name__ == '__main__':
    unittest.main() 