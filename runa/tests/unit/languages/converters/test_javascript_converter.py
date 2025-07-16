#!/usr/bin/env python3
"""
Unit tests for JavaScript ↔ Runa Converter

Tests bidirectional conversion between JavaScript AST and Runa AST,
including JavaScript-specific features like prototypes, closures, and async patterns.
"""

import unittest
from unittest.mock import Mock, patch
from typing import List, Dict, Any
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../src'))

from runa.languages.tier1.javascript.js_converter import JSToRunaConverter, RunaToJSConverter
from runa.languages.tier1.javascript.js_ast import *
from runa.core.runa_ast import *


class TestJSToRunaConverter(unittest.TestCase):
    """Test JavaScript AST to Runa AST conversion."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = JSToRunaConverter()
    
    def test_variable_declaration(self):
        """Test conversion of variable declarations."""
        # JavaScript: let x = 42;
        js_ast = JSProgram([
            JSVariableDeclaration(
                kind='let',
                declarations=[
                    JSVariableDeclarator(
                        id=JSIdentifier(name='x'),
                        init=JSLiteral(value=42)
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(js_ast)
        
        self.assertIsInstance(runa_program, Program)
        self.assertEqual(len(runa_program.statements), 1)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertEqual(stmt.name, 'x')
        self.assertIsInstance(stmt.value, NumericLiteral)
        self.assertEqual(stmt.value.value, 42)
    
    def test_const_declaration(self):
        """Test conversion of const declarations."""
        # JavaScript: const PI = 3.14159;
        js_ast = JSProgram([
            JSVariableDeclaration(
                kind='const',
                declarations=[
                    JSVariableDeclarator(
                        id=JSIdentifier(name='PI'),
                        init=JSLiteral(value=3.14159)
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(js_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertEqual(stmt.name, 'PI')
        self.assertTrue(stmt.is_const)  # Should mark as constant
    
    def test_function_declaration(self):
        """Test conversion of function declaration."""
        # JavaScript: function add(a, b) { return a + b; }
        js_ast = JSProgram([
            JSFunctionDeclaration(
                id=JSIdentifier(name='add'),
                params=[
                    JSIdentifier(name='a'),
                    JSIdentifier(name='b')
                ],
                body=JSBlockStatement([
                    JSReturnStatement(
                        argument=JSBinaryExpression(
                            left=JSIdentifier(name='a'),
                            operator='+',
                            right=JSIdentifier(name='b')
                        )
                    )
                ])
            )
        ])
        
        runa_program = self.converter.convert(js_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, FunctionDeclaration)
        self.assertEqual(stmt.name, 'add')
        self.assertEqual(len(stmt.parameters), 2)
        self.assertEqual(stmt.parameters[0].name, 'a')
        self.assertEqual(stmt.parameters[1].name, 'b')
    
    def test_arrow_function(self):
        """Test conversion of arrow functions."""
        # JavaScript: const square = x => x * x;
        js_ast = JSProgram([
            JSVariableDeclaration(
                kind='const',
                declarations=[
                    JSVariableDeclarator(
                        id=JSIdentifier(name='square'),
                        init=JSArrowFunctionExpression(
                            params=[JSIdentifier(name='x')],
                            body=JSBinaryExpression(
                                left=JSIdentifier(name='x'),
                                operator='*',
                                right=JSIdentifier(name='x')
                            )
                        )
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(js_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        # Arrow function should be converted to function expression
        self.assertIsInstance(stmt.value, FunctionExpression)
    
    def test_object_literal(self):
        """Test conversion of object literals."""
        # JavaScript: const person = { name: "Alice", age: 30 };
        js_ast = JSProgram([
            JSVariableDeclaration(
                kind='const',
                declarations=[
                    JSVariableDeclarator(
                        id=JSIdentifier(name='person'),
                        init=JSObjectExpression([
                            JSProperty(
                                key=JSIdentifier(name='name'),
                                value=JSLiteral(value="Alice")
                            ),
                            JSProperty(
                                key=JSIdentifier(name='age'),
                                value=JSLiteral(value=30)
                            )
                        ])
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(js_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertIsInstance(stmt.value, ObjectLiteral)
        self.assertEqual(len(stmt.value.properties), 2)
    
    def test_array_literal(self):
        """Test conversion of array literals."""
        # JavaScript: const numbers = [1, 2, 3, 4, 5];
        js_ast = JSProgram([
            JSVariableDeclaration(
                kind='const',
                declarations=[
                    JSVariableDeclarator(
                        id=JSIdentifier(name='numbers'),
                        init=JSArrayExpression([
                            JSLiteral(value=1),
                            JSLiteral(value=2),
                            JSLiteral(value=3),
                            JSLiteral(value=4),
                            JSLiteral(value=5)
                        ])
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(js_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertIsInstance(stmt.value, ArrayLiteral)
        self.assertEqual(len(stmt.value.elements), 5)
    
    def test_if_statement(self):
        """Test conversion of if statements."""
        # JavaScript: if (x > 0) { console.log("positive"); }
        js_ast = JSProgram([
            JSIfStatement(
                test=JSBinaryExpression(
                    left=JSIdentifier(name='x'),
                    operator='>',
                    right=JSLiteral(value=0)
                ),
                consequent=JSBlockStatement([
                    JSExpressionStatement(
                        expression=JSCallExpression(
                            callee=JSMemberExpression(
                                object=JSIdentifier(name='console'),
                                property=JSIdentifier(name='log')
                            ),
                            arguments=[JSLiteral(value="positive")]
                        )
                    )
                ])
            )
        ])
        
        runa_program = self.converter.convert(js_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, IfStatement)
        self.assertIsInstance(stmt.condition, BinaryOperation)
    
    def test_for_loop(self):
        """Test conversion of for loops."""
        # JavaScript: for (let i = 0; i < 10; i++) { console.log(i); }
        js_ast = JSProgram([
            JSForStatement(
                init=JSVariableDeclaration(
                    kind='let',
                    declarations=[
                        JSVariableDeclarator(
                            id=JSIdentifier(name='i'),
                            init=JSLiteral(value=0)
                        )
                    ]
                ),
                test=JSBinaryExpression(
                    left=JSIdentifier(name='i'),
                    operator='<',
                    right=JSLiteral(value=10)
                ),
                update=JSUpdateExpression(
                    operator='++',
                    argument=JSIdentifier(name='i')
                ),
                body=JSBlockStatement([
                    JSExpressionStatement(
                        expression=JSCallExpression(
                            callee=JSMemberExpression(
                                object=JSIdentifier(name='console'),
                                property=JSIdentifier(name='log')
                            ),
                            arguments=[JSIdentifier(name='i')]
                        )
                    )
                ])
            )
        ])
        
        runa_program = self.converter.convert(js_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, ForStatement)
    
    def test_try_catch(self):
        """Test conversion of try-catch statements."""
        # JavaScript: try { risky(); } catch (e) { handle(e); }
        js_ast = JSProgram([
            JSTryStatement(
                block=JSBlockStatement([
                    JSExpressionStatement(
                        expression=JSCallExpression(
                            callee=JSIdentifier(name='risky'),
                            arguments=[]
                        )
                    )
                ]),
                handler=JSCatchClause(
                    param=JSIdentifier(name='e'),
                    body=JSBlockStatement([
                        JSExpressionStatement(
                            expression=JSCallExpression(
                                callee=JSIdentifier(name='handle'),
                                arguments=[JSIdentifier(name='e')]
                            )
                        )
                    ])
                )
            )
        ])
        
        runa_program = self.converter.convert(js_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, TryStatement)
        self.assertEqual(len(stmt.handlers), 1)
    
    def test_async_function(self):
        """Test conversion of async functions."""
        # JavaScript: async function fetchData() { return await fetch('/api'); }
        js_ast = JSProgram([
            JSFunctionDeclaration(
                id=JSIdentifier(name='fetchData'),
                params=[],
                body=JSBlockStatement([
                    JSReturnStatement(
                        argument=JSAwaitExpression(
                            argument=JSCallExpression(
                                callee=JSIdentifier(name='fetch'),
                                arguments=[JSLiteral(value='/api')]
                            )
                        )
                    )
                ]),
                is_async=True
            )
        ])
        
        runa_program = self.converter.convert(js_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, FunctionDeclaration)
        self.assertTrue(stmt.is_async)
    
    def test_class_declaration(self):
        """Test conversion of class declarations."""
        # JavaScript: class Person { constructor(name) { this.name = name; } }
        js_ast = JSProgram([
            JSClassDeclaration(
                id=JSIdentifier(name='Person'),
                body=JSClassBody([
                    JSMethodDefinition(
                        key=JSIdentifier(name='constructor'),
                        value=JSFunctionExpression(
                            params=[JSIdentifier(name='name')],
                            body=JSBlockStatement([
                                JSExpressionStatement(
                                    expression=JSAssignmentExpression(
                                        left=JSMemberExpression(
                                            object=JSThisExpression(),
                                            property=JSIdentifier(name='name')
                                        ),
                                        operator='=',
                                        right=JSIdentifier(name='name')
                                    )
                                )
                            ])
                        ),
                        kind='constructor'
                    )
                ])
            )
        ])
        
        runa_program = self.converter.convert(js_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, ClassDeclaration)
        self.assertEqual(stmt.name, 'Person')
    
    def test_destructuring_assignment(self):
        """Test conversion of destructuring assignments."""
        # JavaScript: const { name, age } = person;
        js_ast = JSProgram([
            JSVariableDeclaration(
                kind='const',
                declarations=[
                    JSVariableDeclarator(
                        id=JSObjectPattern([
                            JSProperty(
                                key=JSIdentifier(name='name'),
                                value=JSIdentifier(name='name')
                            ),
                            JSProperty(
                                key=JSIdentifier(name='age'),
                                value=JSIdentifier(name='age')
                            )
                        ]),
                        init=JSIdentifier(name='person')
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(js_ast)
        
        # Destructuring should be converted to multiple variable assignments
        self.assertIsInstance(runa_program, Program)
        self.assertGreater(len(runa_program.statements), 0)
    
    def test_template_literals(self):
        """Test conversion of template literals."""
        # JavaScript: const message = `Hello, ${name}!`;
        js_ast = JSProgram([
            JSVariableDeclaration(
                kind='const',
                declarations=[
                    JSVariableDeclarator(
                        id=JSIdentifier(name='message'),
                        init=JSTemplateLiteral(
                            quasis=[
                                JSTemplateElement(value='Hello, '),
                                JSTemplateElement(value='!')
                            ],
                            expressions=[JSIdentifier(name='name')]
                        )
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(js_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        # Template literal should be converted to string concatenation
        self.assertIsInstance(stmt.value, (StringLiteral, BinaryOperation))


class TestRunaToJSConverter(unittest.TestCase):
    """Test Runa AST to JavaScript AST conversion."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = RunaToJSConverter()
    
    def test_variable_declaration_conversion(self):
        """Test conversion of variable declarations."""
        # Runa: Let x be 42
        runa_program = Program([
            VariableDeclaration(
                name='x',
                value=NumericLiteral(value=42)
            )
        ])
        
        js_program = self.converter.convert(runa_program)
        
        self.assertIsInstance(js_program, JSProgram)
        self.assertEqual(len(js_program.body), 1)
        
        stmt = js_program.body[0]
        self.assertIsInstance(stmt, JSVariableDeclaration)
        self.assertEqual(stmt.kind, 'let')
        self.assertEqual(stmt.declarations[0].id.name, 'x')
    
    def test_const_declaration_conversion(self):
        """Test conversion of constant declarations."""
        # Runa: Set PI as constant to 3.14159
        runa_program = Program([
            VariableDeclaration(
                name='PI',
                value=NumericLiteral(value=3.14159),
                is_const=True
            )
        ])
        
        js_program = self.converter.convert(runa_program)
        
        stmt = js_program.body[0]
        self.assertIsInstance(stmt, JSVariableDeclaration)
        self.assertEqual(stmt.kind, 'const')
    
    def test_function_declaration_conversion(self):
        """Test conversion of function declarations."""
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
        
        js_program = self.converter.convert(runa_program)
        
        stmt = js_program.body[0]
        self.assertIsInstance(stmt, JSFunctionDeclaration)
        self.assertEqual(stmt.id.name, 'add')
        self.assertEqual(len(stmt.params), 2)
    
    def test_async_function_conversion(self):
        """Test conversion of async functions."""
        # Runa: Define async fetchData: Return await fetch("/api")
        runa_program = Program([
            FunctionDeclaration(
                name='fetchData',
                parameters=[],
                body=[
                    ReturnStatement(
                        value=AwaitExpression(
                            expression=FunctionCall(
                                function=Identifier(name='fetch'),
                                arguments=[StringLiteral(value='/api')]
                            )
                        )
                    )
                ],
                is_async=True
            )
        ])
        
        js_program = self.converter.convert(runa_program)
        
        stmt = js_program.body[0]
        self.assertIsInstance(stmt, JSFunctionDeclaration)
        self.assertTrue(stmt.is_async)
    
    def test_if_statement_conversion(self):
        """Test conversion of if statements."""
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
        
        js_program = self.converter.convert(runa_program)
        
        stmt = js_program.body[0]
        self.assertIsInstance(stmt, JSIfStatement)
        self.assertIsInstance(stmt.test, JSBinaryExpression)
        self.assertEqual(stmt.test.operator, '>')
    
    def test_object_literal_conversion(self):
        """Test conversion of object literals."""
        # Runa: Let person be object with name "Alice" and age 30
        runa_program = Program([
            VariableDeclaration(
                name='person',
                value=ObjectLiteral([
                    ObjectProperty(
                        key='name',
                        value=StringLiteral(value="Alice")
                    ),
                    ObjectProperty(
                        key='age',
                        value=NumericLiteral(value=30)
                    )
                ])
            )
        ])
        
        js_program = self.converter.convert(runa_program)
        
        stmt = js_program.body[0]
        self.assertIsInstance(stmt, JSVariableDeclaration)
        self.assertIsInstance(stmt.declarations[0].init, JSObjectExpression)
    
    def test_array_literal_conversion(self):
        """Test conversion of array literals."""
        # Runa: Let numbers be list containing 1, 2, 3, 4, 5
        runa_program = Program([
            VariableDeclaration(
                name='numbers',
                value=ArrayLiteral([
                    NumericLiteral(value=1),
                    NumericLiteral(value=2),
                    NumericLiteral(value=3),
                    NumericLiteral(value=4),
                    NumericLiteral(value=5)
                ])
            )
        ])
        
        js_program = self.converter.convert(runa_program)
        
        stmt = js_program.body[0]
        self.assertIsInstance(stmt, JSVariableDeclaration)
        self.assertIsInstance(stmt.declarations[0].init, JSArrayExpression)
        self.assertEqual(len(stmt.declarations[0].init.elements), 5)


class TestJavaScriptSpecificFeatures(unittest.TestCase):
    """Test JavaScript-specific language features."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.js_to_runa = JSToRunaConverter()
        self.runa_to_js = RunaToJSConverter()
    
    def test_closure_conversion(self):
        """Test conversion of closures."""
        # JavaScript: function outer() { let x = 1; return function() { return x; }; }
        js_ast = JSProgram([
            JSFunctionDeclaration(
                id=JSIdentifier(name='outer'),
                params=[],
                body=JSBlockStatement([
                    JSVariableDeclaration(
                        kind='let',
                        declarations=[
                            JSVariableDeclarator(
                                id=JSIdentifier(name='x'),
                                init=JSLiteral(value=1)
                            )
                        ]
                    ),
                    JSReturnStatement(
                        argument=JSFunctionExpression(
                            params=[],
                            body=JSBlockStatement([
                                JSReturnStatement(
                                    argument=JSIdentifier(name='x')
                                )
                            ])
                        )
                    )
                ])
            )
        ])
        
        runa_program = self.js_to_runa.convert(js_ast)
        
        # Should preserve closure semantics
        self.assertIsInstance(runa_program, Program)
        func_def = runa_program.statements[0]
        self.assertIsInstance(func_def, FunctionDeclaration)
    
    def test_prototype_inheritance(self):
        """Test handling of prototype-based inheritance."""
        # JavaScript: Person.prototype.greet = function() { return `Hello, ${this.name}`; };
        js_ast = JSProgram([
            JSExpressionStatement(
                expression=JSAssignmentExpression(
                    left=JSMemberExpression(
                        object=JSMemberExpression(
                            object=JSIdentifier(name='Person'),
                            property=JSIdentifier(name='prototype')
                        ),
                        property=JSIdentifier(name='greet')
                    ),
                    operator='=',
                    right=JSFunctionExpression(
                        params=[],
                        body=JSBlockStatement([
                            JSReturnStatement(
                                argument=JSTemplateLiteral(
                                    quasis=[
                                        JSTemplateElement(value='Hello, '),
                                        JSTemplateElement(value='')
                                    ],
                                    expressions=[
                                        JSMemberExpression(
                                            object=JSThisExpression(),
                                            property=JSIdentifier(name='name')
                                        )
                                    ]
                                )
                            )
                        ])
                    )
                )
            )
        ])
        
        runa_program = self.js_to_runa.convert(js_ast)
        
        # Should convert to method definition or equivalent
        self.assertIsInstance(runa_program, Program)
        self.assertGreater(len(runa_program.statements), 0)
    
    def test_callback_patterns(self):
        """Test conversion of callback patterns."""
        # JavaScript: setTimeout(() => console.log("done"), 1000);
        js_ast = JSProgram([
            JSExpressionStatement(
                expression=JSCallExpression(
                    callee=JSIdentifier(name='setTimeout'),
                    arguments=[
                        JSArrowFunctionExpression(
                            params=[],
                            body=JSCallExpression(
                                callee=JSMemberExpression(
                                    object=JSIdentifier(name='console'),
                                    property=JSIdentifier(name='log')
                                ),
                                arguments=[JSLiteral(value="done")]
                            )
                        ),
                        JSLiteral(value=1000)
                    ]
                )
            )
        ])
        
        runa_program = self.js_to_runa.convert(js_ast)
        
        # Should preserve callback semantics
        self.assertIsInstance(runa_program, Program)
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, ExpressionStatement)
    
    def test_hoisting_implications(self):
        """Test handling of JavaScript hoisting implications."""
        # JavaScript with hoisting: console.log(x); var x = 5;
        js_ast = JSProgram([
            JSExpressionStatement(
                expression=JSCallExpression(
                    callee=JSMemberExpression(
                        object=JSIdentifier(name='console'),
                        property=JSIdentifier(name='log')
                    ),
                    arguments=[JSIdentifier(name='x')]
                )
            ),
            JSVariableDeclaration(
                kind='var',
                declarations=[
                    JSVariableDeclarator(
                        id=JSIdentifier(name='x'),
                        init=JSLiteral(value=5)
                    )
                ]
            )
        ])
        
        runa_program = self.js_to_runa.convert(js_ast)
        
        # Should handle hoisting semantics appropriately
        self.assertIsInstance(runa_program, Program)
        self.assertEqual(len(runa_program.statements), 2)


class TestJavaScriptRoundTrip(unittest.TestCase):
    """Test round-trip conversion for JavaScript-specific patterns."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.js_to_runa = JSToRunaConverter()
        self.runa_to_js = RunaToJSConverter()
    
    def test_roundtrip_arrow_function(self):
        """Test round-trip conversion of arrow functions."""
        original_js = JSProgram([
            JSVariableDeclaration(
                kind='const',
                declarations=[
                    JSVariableDeclarator(
                        id=JSIdentifier(name='add'),
                        init=JSArrowFunctionExpression(
                            params=[JSIdentifier(name='a'), JSIdentifier(name='b')],
                            body=JSBinaryExpression(
                                left=JSIdentifier(name='a'),
                                operator='+',
                                right=JSIdentifier(name='b')
                            )
                        )
                    )
                ]
            )
        ])
        
        # Round-trip conversion
        runa_program = self.js_to_runa.convert(original_js)
        converted_js = self.runa_to_js.convert(runa_program)
        
        # Verify function structure is preserved
        self.assertIsInstance(converted_js, JSProgram)
        stmt = converted_js.body[0]
        self.assertIsInstance(stmt, JSVariableDeclaration)
        # May be converted to regular function expression
        self.assertIsInstance(stmt.declarations[0].init, (JSArrowFunctionExpression, JSFunctionExpression))
    
    def test_roundtrip_object_method(self):
        """Test round-trip conversion of object methods."""
        original_js = JSProgram([
            JSVariableDeclaration(
                kind='const',
                declarations=[
                    JSVariableDeclarator(
                        id=JSIdentifier(name='obj'),
                        init=JSObjectExpression([
                            JSProperty(
                                key=JSIdentifier(name='method'),
                                value=JSFunctionExpression(
                                    params=[],
                                    body=JSBlockStatement([
                                        JSReturnStatement(
                                            argument=JSLiteral(value="result")
                                        )
                                    ])
                                )
                            )
                        ])
                    )
                ]
            )
        ])
        
        # Round-trip conversion
        runa_program = self.js_to_runa.convert(original_js)
        converted_js = self.runa_to_js.convert(runa_program)
        
        # Verify object structure is preserved
        self.assertIsInstance(converted_js, JSProgram)
        stmt = converted_js.body[0]
        self.assertIsInstance(stmt, JSVariableDeclaration)
        self.assertIsInstance(stmt.declarations[0].init, JSObjectExpression)


if __name__ == '__main__':
    unittest.main()