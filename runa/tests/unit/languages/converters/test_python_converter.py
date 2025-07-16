#!/usr/bin/env python3
"""
Unit tests for Python ↔ Runa Converter

Tests bidirectional conversion between Python AST and Runa AST,
ensuring semantic preservation and round-trip accuracy.
"""

import unittest
from unittest.mock import Mock, patch
from typing import List, Dict, Any
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../src'))

from runa.languages.tier1.python.py_converter import PyToRunaConverter, RunaToPyConverter
from runa.languages.tier1.python.py_ast import *
from runa.core.runa_ast import *


class TestPyToRunaConverter(unittest.TestCase):
    """Test Python AST to Runa AST conversion."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = PyToRunaConverter()
    
    def test_simple_variable_assignment(self):
        """Test conversion of simple variable assignment."""
        # Python: x = 42
        py_ast = PyModule([
            PyAssign(
                targets=[PyName(id='x')],
                value=PyConstant(value=42)
            )
        ])
        
        runa_program = self.converter.convert(py_ast)
        
        self.assertIsInstance(runa_program, Program)
        self.assertEqual(len(runa_program.statements), 1)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertEqual(stmt.name, 'x')
        self.assertIsInstance(stmt.value, NumericLiteral)
        self.assertEqual(stmt.value.value, 42)
    
    def test_typed_variable_assignment(self):
        """Test conversion of typed variable assignment."""
        # Python: x: int = 42
        py_ast = PyModule([
            PyAnnAssign(
                target=PyName(id='x'),
                annotation=PyName(id='int'),
                value=PyConstant(value=42)
            )
        ])
        
        runa_program = self.converter.convert(py_ast)
        
        self.assertIsInstance(runa_program, Program)
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertEqual(stmt.name, 'x')
        self.assertIsInstance(stmt.type_annotation, TypeReference)
        self.assertEqual(stmt.type_annotation.name, 'int')
    
    def test_function_definition(self):
        """Test conversion of function definition."""
        # Python: def add(a, b): return a + b
        py_ast = PyModule([
            PyFunctionDef(
                name='add',
                args=PyArguments([
                    PyArg(arg='a'),
                    PyArg(arg='b')
                ]),
                body=[
                    PyReturn(
                        value=PyBinOp(
                            left=PyName(id='a'),
                            op=PyAdd(),
                            right=PyName(id='b')
                        )
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(py_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, FunctionDeclaration)
        self.assertEqual(stmt.name, 'add')
        self.assertEqual(len(stmt.parameters), 2)
        self.assertEqual(stmt.parameters[0].name, 'a')
        self.assertEqual(stmt.parameters[1].name, 'b')
        
        # Check function body
        self.assertEqual(len(stmt.body), 1)
        return_stmt = stmt.body[0]
        self.assertIsInstance(return_stmt, ReturnStatement)
        self.assertIsInstance(return_stmt.value, BinaryOperation)
    
    def test_if_statement(self):
        """Test conversion of if statement."""
        # Python: if x > 0: print("positive")
        py_ast = PyModule([
            PyIf(
                test=PyCompare(
                    left=PyName(id='x'),
                    ops=[PyGt()],
                    comparators=[PyConstant(value=0)]
                ),
                body=[
                    PyExpr(
                        value=PyCall(
                            func=PyName(id='print'),
                            args=[PyConstant(value="positive")]
                        )
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(py_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, IfStatement)
        self.assertIsInstance(stmt.condition, BinaryOperation)
        self.assertEqual(len(stmt.then_body), 1)
    
    def test_class_definition(self):
        """Test conversion of class definition."""
        # Python: class Person: pass
        py_ast = PyModule([
            PyClassDef(
                name='Person',
                bases=[],
                body=[PyPass()]
            )
        ])
        
        runa_program = self.converter.convert(py_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, ClassDeclaration)
        self.assertEqual(stmt.name, 'Person')
    
    def test_list_comprehension(self):
        """Test conversion of list comprehension."""
        # Python: [x * 2 for x in range(10)]
        py_ast = PyModule([
            PyExpr(
                value=PyListComp(
                    elt=PyBinOp(
                        left=PyName(id='x'),
                        op=PyMult(),
                        right=PyConstant(value=2)
                    ),
                    generators=[
                        PyComprehension(
                            target=PyName(id='x'),
                            iter=PyCall(
                                func=PyName(id='range'),
                                args=[PyConstant(value=10)]
                            )
                        )
                    ]
                )
            )
        ])
        
        runa_program = self.converter.convert(py_ast)
        
        # List comprehensions should be converted to equivalent loops or functional patterns
        self.assertIsInstance(runa_program, Program)
        self.assertGreater(len(runa_program.statements), 0)
    
    def test_exception_handling(self):
        """Test conversion of try-except blocks."""
        # Python: try: risky() except Exception: handle()
        py_ast = PyModule([
            PyTry(
                body=[
                    PyExpr(
                        value=PyCall(func=PyName(id='risky'), args=[])
                    )
                ],
                handlers=[
                    PyExceptHandler(
                        type=PyName(id='Exception'),
                        body=[
                            PyExpr(
                                value=PyCall(func=PyName(id='handle'), args=[])
                            )
                        ]
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(py_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, TryStatement)
        self.assertEqual(len(stmt.body), 1)
        self.assertEqual(len(stmt.handlers), 1)
    
    def test_async_function(self):
        """Test conversion of async function."""
        # Python: async def fetch(): await api_call()
        py_ast = PyModule([
            PyAsyncFunctionDef(
                name='fetch',
                args=PyArguments([]),
                body=[
                    PyExpr(
                        value=PyAwait(
                            value=PyCall(func=PyName(id='api_call'), args=[])
                        )
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(py_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, FunctionDeclaration)
        self.assertTrue(stmt.is_async)
    
    def test_import_statement(self):
        """Test conversion of import statements."""
        # Python: import os, from sys import path
        py_ast = PyModule([
            PyImport(names=[PyAlias(name='os')]),
            PyImportFrom(
                module='sys',
                names=[PyAlias(name='path')]
            )
        ])
        
        runa_program = self.converter.convert(py_ast)
        
        # Imports should be converted to appropriate Runa imports
        self.assertGreater(len(runa_program.statements), 0)
        
        # Check that import statements are preserved
        import_stmts = [s for s in runa_program.statements if isinstance(s, ImportStatement)]
        self.assertGreater(len(import_stmts), 0)


class TestRunaToPyConverter(unittest.TestCase):
    """Test Runa AST to Python AST conversion."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = RunaToPyConverter()
    
    def test_simple_variable_declaration(self):
        """Test conversion of simple variable declaration."""
        # Runa: Let x be 42
        runa_program = Program([
            VariableDeclaration(
                name='x',
                value=NumericLiteral(value=42)
            )
        ])
        
        py_module = self.converter.convert(runa_program)
        
        self.assertIsInstance(py_module, PyModule)
        self.assertEqual(len(py_module.body), 1)
        
        stmt = py_module.body[0]
        self.assertIsInstance(stmt, PyAssign)
        self.assertEqual(stmt.targets[0].id, 'x')
        self.assertEqual(stmt.value.value, 42)
    
    def test_typed_variable_declaration(self):
        """Test conversion of typed variable declaration."""
        # Runa: Let x as Integer be 42
        runa_program = Program([
            VariableDeclaration(
                name='x',
                type_annotation=TypeReference(name='Integer'),
                value=NumericLiteral(value=42)
            )
        ])
        
        py_module = self.converter.convert(runa_program)
        
        stmt = py_module.body[0]
        self.assertIsInstance(stmt, PyAnnAssign)
        self.assertEqual(stmt.target.id, 'x')
        self.assertEqual(stmt.annotation.id, 'int')  # Integer -> int mapping
    
    def test_function_declaration(self):
        """Test conversion of function declaration."""
        # Runa: Define add with a and b: Return a plus b
        runa_program = Program([
            FunctionDeclaration(
                name='add',
                parameters=[
                    Parameter(name='a'),
                    Parameter(name='b')
                ],
                body=[
                    ReturnStatement(
                        value=BinaryOperation(
                            left=Identifier(name='a'),
                            operator='plus',
                            right=Identifier(name='b')
                        )
                    )
                ]
            )
        ])
        
        py_module = self.converter.convert(runa_program)
        
        stmt = py_module.body[0]
        self.assertIsInstance(stmt, PyFunctionDef)
        self.assertEqual(stmt.name, 'add')
        self.assertEqual(len(stmt.args.args), 2)
        self.assertEqual(stmt.args.args[0].arg, 'a')
        self.assertEqual(stmt.args.args[1].arg, 'b')
    
    def test_if_statement_conversion(self):
        """Test conversion of if statement."""
        # Runa: If x is greater than 0: Display "positive"
        runa_program = Program([
            IfStatement(
                condition=BinaryOperation(
                    left=Identifier(name='x'),
                    operator='is greater than',
                    right=NumericLiteral(value=0)
                ),
                then_body=[
                    ExpressionStatement(
                        expression=FunctionCall(
                            function=Identifier(name='display'),
                            arguments=[StringLiteral(value="positive")]
                        )
                    )
                ]
            )
        ])
        
        py_module = self.converter.convert(runa_program)
        
        stmt = py_module.body[0]
        self.assertIsInstance(stmt, PyIf)
        self.assertIsInstance(stmt.test, PyCompare)
    
    def test_class_declaration(self):
        """Test conversion of class declaration."""
        # Runa: Define type Person with properties name
        runa_program = Program([
            ClassDeclaration(
                name='Person',
                properties=[
                    PropertyDeclaration(
                        name='name',
                        type_annotation=TypeReference(name='String')
                    )
                ]
            )
        ])
        
        py_module = self.converter.convert(runa_program)
        
        stmt = py_module.body[0]
        self.assertIsInstance(stmt, PyClassDef)
        self.assertEqual(stmt.name, 'Person')
    
    def test_error_handling_conversion(self):
        """Test conversion of error handling."""
        # Runa: Try: risky operation Catch error: handle error
        runa_program = Program([
            TryStatement(
                body=[
                    ExpressionStatement(
                        expression=FunctionCall(
                            function=Identifier(name='risky_operation'),
                            arguments=[]
                        )
                    )
                ],
                handlers=[
                    CatchClause(
                        exception_type=TypeReference(name='Error'),
                        variable_name='error',
                        body=[
                            ExpressionStatement(
                                expression=FunctionCall(
                                    function=Identifier(name='handle_error'),
                                    arguments=[Identifier(name='error')]
                                )
                            )
                        ]
                    )
                ]
            )
        ])
        
        py_module = self.converter.convert(runa_program)
        
        stmt = py_module.body[0]
        self.assertIsInstance(stmt, PyTry)
        self.assertEqual(len(stmt.handlers), 1)


class TestBidirectionalConversion(unittest.TestCase):
    """Test round-trip conversion accuracy."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.py_to_runa = PyToRunaConverter()
        self.runa_to_py = RunaToPyConverter()
    
    def test_roundtrip_simple_assignment(self):
        """Test round-trip conversion of simple assignment."""
        # Start with Python AST
        original_py = PyModule([
            PyAssign(
                targets=[PyName(id='x')],
                value=PyConstant(value=42)
            )
        ])
        
        # Convert to Runa and back
        runa_program = self.py_to_runa.convert(original_py)
        converted_py = self.runa_to_py.convert(runa_program)
        
        # Check semantic equivalence
        self.assertIsInstance(converted_py, PyModule)
        self.assertEqual(len(converted_py.body), 1)
        
        stmt = converted_py.body[0]
        self.assertIsInstance(stmt, PyAssign)
        self.assertEqual(stmt.targets[0].id, 'x')
        self.assertEqual(stmt.value.value, 42)
    
    def test_roundtrip_function_definition(self):
        """Test round-trip conversion of function definition."""
        original_py = PyModule([
            PyFunctionDef(
                name='add',
                args=PyArguments([
                    PyArg(arg='a'),
                    PyArg(arg='b')
                ]),
                body=[
                    PyReturn(
                        value=PyBinOp(
                            left=PyName(id='a'),
                            op=PyAdd(),
                            right=PyName(id='b')
                        )
                    )
                ]
            )
        ])
        
        # Round-trip conversion
        runa_program = self.py_to_runa.convert(original_py)
        converted_py = self.runa_to_py.convert(runa_program)
        
        # Verify function structure is preserved
        self.assertIsInstance(converted_py, PyModule)
        stmt = converted_py.body[0]
        self.assertIsInstance(stmt, PyFunctionDef)
        self.assertEqual(stmt.name, 'add')
        self.assertEqual(len(stmt.args.args), 2)
    
    def test_semantic_preservation(self):
        """Test that semantic meaning is preserved during conversion."""
        # Complex example with multiple constructs
        original_py = PyModule([
            PyFunctionDef(
                name='fibonacci',
                args=PyArguments([PyArg(arg='n')]),
                body=[
                    PyIf(
                        test=PyCompare(
                            left=PyName(id='n'),
                            ops=[PyLtE()],
                            comparators=[PyConstant(value=1)]
                        ),
                        body=[PyReturn(value=PyName(id='n'))],
                        orelse=[
                            PyReturn(
                                value=PyBinOp(
                                    left=PyCall(
                                        func=PyName(id='fibonacci'),
                                        args=[PyBinOp(
                                            left=PyName(id='n'),
                                            op=PySub(),
                                            right=PyConstant(value=1)
                                        )]
                                    ),
                                    op=PyAdd(),
                                    right=PyCall(
                                        func=PyName(id='fibonacci'),
                                        args=[PyBinOp(
                                            left=PyName(id='n'),
                                            op=PySub(),
                                            right=PyConstant(value=2)
                                        )]
                                    )
                                )
                            )
                        ]
                    )
                ]
            )
        ])
        
        # Convert and verify structure preservation
        runa_program = self.py_to_runa.convert(original_py)
        converted_py = self.runa_to_py.convert(runa_program)
        
        # Check that the recursive structure is maintained
        self.assertIsInstance(converted_py, PyModule)
        func_def = converted_py.body[0]
        self.assertIsInstance(func_def, PyFunctionDef)
        self.assertEqual(func_def.name, 'fibonacci')
        
        # Verify the if statement structure
        if_stmt = func_def.body[0]
        self.assertIsInstance(if_stmt, PyIf)
        self.assertIsNotNone(if_stmt.orelse)


class TestConverterErrorHandling(unittest.TestCase):
    """Test error handling in converters."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = PyToRunaConverter()
    
    def test_invalid_ast_node(self):
        """Test handling of invalid AST nodes."""
        # Create mock invalid node
        invalid_node = Mock()
        invalid_node.__class__.__name__ = 'InvalidNode'
        
        py_ast = PyModule([invalid_node])
        
        # Should handle gracefully without crashing
        result = self.converter.convert(py_ast)
        self.assertIsInstance(result, Program)
    
    def test_malformed_function(self):
        """Test handling of malformed function definitions."""
        # Function with no name
        py_ast = PyModule([
            PyFunctionDef(
                name='',  # Empty name
                args=PyArguments([]),
                body=[]
            )
        ])
        
        # Should handle gracefully
        result = self.converter.convert(py_ast)
        self.assertIsInstance(result, Program)
    
    def test_nested_complexity(self):
        """Test handling of deeply nested structures."""
        # Create deeply nested expression
        def create_nested_binop(depth):
            if depth == 0:
                return PyConstant(value=1)
            return PyBinOp(
                left=create_nested_binop(depth - 1),
                op=PyAdd(),
                right=PyConstant(value=1)
            )
        
        py_ast = PyModule([
            PyExpr(value=create_nested_binop(50))  # Deep nesting
        ])
        
        # Should handle without stack overflow
        result = self.converter.convert(py_ast)
        self.assertIsInstance(result, Program)


if __name__ == '__main__':
    unittest.main()